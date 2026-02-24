# Notes on Django tests

## How Django suggests implementing tests

Django's testing framework is built on top of Python's standard `unittest` module.
Django extends it with a test runner, a test client for simulating HTTP requests,
and helpers for working with the database in isolation.

The recommended workflow is:

1. Write test classes that extend `django.test.TestCase` (or a subclass thereof).
2. Place test code in `tests.py` inside each app, or inside a `tests/` package
   (a directory containing an `__init__.py` and one file per category of tests,
   e.g. `tests/test_models.py`, `tests/test_views.py`, …).
3. Run the suite with the management command:

```bash
uv run manage.py test
# or, to target a single app:
uv run manage.py test accounts
# or a single module/class/method:
uv run manage.py test accounts.tests.test_models.CustomUserModelTest
```

Each test class wraps every test method in a database transaction that is rolled
back automatically after the method returns, so tests are isolated and the
database is left clean.

### Test discovery rules

Django (and `unittest`) discovers tests by looking for:
- files whose name starts with `test` (e.g. `test_models.py`)
- classes that inherit from `unittest.TestCase` (or any subclass)
- methods whose name starts with `test`

---

## Kinds of testing available in a Django project

| Kind | Scope | Django entry-point |
|---|---|---|
| **Unit tests – models** | A single model class and its methods | `TestCase` |
| **Unit tests – validators / utils** | A standalone function or class | `TestCase` / `SimpleTestCase` |
| **Unit tests – forms** | A `Form` or `ModelForm` class | `TestCase` |
| **Integration tests – views** | A URL + view + template rendering | `TestCase` + `Client` |
| **API tests** | REST endpoints (JSON in / JSON out) | `APITestCase` (DRF) |
| **Database / query tests** | ORM behaviour, constraints, signals | `TestCase` / `TransactionTestCase` |
| **Browser / end-to-end tests** | Full browser interaction with the running app | Selenium / Playwright |
| **Performance / load tests** | Throughput, latency under load | Locust / k6 |
| **Security tests** | Auth, permissions, injection | manual + Bandit / OWASP ZAP |

---

## Unit tests – models

Model tests verify that:
- instances can be created and persisted correctly,
- field constraints (blank, null, unique, max_length, …) are enforced,
- `__str__` and other custom methods return the expected values,
- validators attached to fields raise `ValidationError` for invalid input.

```python
# accounts/tests/test_models.py
from django.test import TestCase
from django.core.exceptions import ValidationError
from accounts.models import CustomUser, Profile


class CustomUserModelTest(TestCase):

    def setUp(self):
        self.user = CustomUser.objects.create_user(
            username="alice",
            email="alice@example.com",
            password="StrongPass123!",
        )

    def test_str_returns_username(self):
        self.assertEqual(str(self.user), "alice")

    def test_email_is_unique(self):
        with self.assertRaises(Exception):
            CustomUser.objects.create_user(
                username="alice2",
                email="alice@example.com",  # duplicate
                password="AnotherPass456!",
            )

    def test_first_name_validator_rejects_digits(self):
        self.user.first_name = "Al1ce"
        with self.assertRaises(ValidationError):
            self.user.full_clean()
```

### Tools / libraries

| Tool | Role |
|---|---|
| `django.test.TestCase` | Base class; wraps every test in a transaction |
| `factory_boy` | Creates model instances with sensible defaults (see below) |
| `Faker` | Generates realistic fake data for fields |
| `mixer` | Alternative to `factory_boy` for quick fixture creation |

#### `factory_boy` example

```python
# accounts/tests/factories.py
import factory
from accounts.models import CustomUser, Profile


class CustomUserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = CustomUser

    username = factory.Sequence(lambda n: f"user_{n}")
    email = factory.LazyAttribute(lambda o: f"{o.username}@example.com")
    password = factory.PostGenerationMethodCall("set_password", "Pass1234!")


class ProfileFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Profile

    user = factory.SubFactory(CustomUserFactory)
    display_name = factory.Sequence(lambda n: f"display_{n}")
```

---

## Unit tests – validators and utility functions

Pure Python functions (validators, helpers, …) can be tested with
`django.test.SimpleTestCase`, which skips all database set-up and is therefore
faster.

```python
# accounts/tests/test_validators.py
from django.test import SimpleTestCase
from django.core.exceptions import ValidationError
from accounts.validators import person_name_validator


class PersonNameValidatorTest(SimpleTestCase):

    def test_valid_name_passes(self):
        # Should not raise
        person_name_validator("Marie-Curie")

    def test_name_with_digits_raises(self):
        with self.assertRaises(ValidationError):
            person_name_validator("J0hn")

    def test_empty_string_behaviour(self):
        # Document whether empty strings are accepted or rejected
        person_name_validator("")  # adjust assertion to match actual behaviour
```

### Tools / libraries

| Tool | Role |
|---|---|
| `django.test.SimpleTestCase` | Base class; **no** database access |
| `pytest` + `pytest-django` | Alternative runner with fixture injection and richer assertions |
| `hypothesis` | Property-based testing – generates many inputs automatically |

---

## Unit tests – forms

Form tests verify that:
- a form is valid when given correct data,
- a form is invalid (and produces the right error messages) for bad data,
- `save()` creates / updates the database record.

```python
# accounts/tests/test_forms.py
from django.test import TestCase
from django.contrib.auth.forms import UserCreationForm


class UserCreationFormTest(TestCase):

    def test_valid_data_creates_user(self):
        form = UserCreationForm(data={
            "username": "bob",
            "password1": "ComplexPass99!",
            "password2": "ComplexPass99!",
        })
        self.assertTrue(form.is_valid())

    def test_password_mismatch_is_invalid(self):
        form = UserCreationForm(data={
            "username": "bob",
            "password1": "ComplexPass99!",
            "password2": "WrongPass",
        })
        self.assertFalse(form.is_valid())
        self.assertIn("password2", form.errors)
```

### Tools / libraries

| Tool | Role |
|---|---|
| `django.test.TestCase` | Provides `assertFormError` and database support |
| `factory_boy` | Supplies initial data dictionaries via `factory.build()` |

---

## Integration tests – views

View tests exercise the full Django request/response cycle: URL routing,
view logic, template rendering, redirects, status codes, and context data.
`django.test.TestCase` provides a built-in `self.client` (an instance of
`django.test.Client`).

```python
# accounts/tests/test_views.py
from django.test import TestCase
from django.urls import reverse
from accounts.tests.factories import CustomUserFactory


class LoginViewTest(TestCase):

    def setUp(self):
        self.user = CustomUserFactory(username="carol")
        self.user.set_password("Pass1234!")
        self.user.save()
        self.url = reverse("login")  # adjust to actual URL name

    def test_login_page_loads(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_valid_credentials_redirect(self):
        response = self.client.post(self.url, {
            "username": "carol",
            "password": "Pass1234!",
        })
        self.assertRedirects(response, reverse("home"))  # adjust target

    def test_invalid_credentials_return_form_errors(self):
        response = self.client.post(self.url, {
            "username": "carol",
            "password": "wrong",
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "error")  # adjust to actual copy
```

### Tools / libraries

| Tool | Role |
|---|---|
| `django.test.Client` | Simulates GET / POST / … requests without a real HTTP server |
| `django.test.TestCase` | Provides `assertRedirects`, `assertContains`, `assertTemplateUsed` |
| `pytest-django` | `rf` fixture (RequestFactory), `client` fixture, `django_db` marker |
| `django.test.RequestFactory` | Builds request objects directly (faster than `Client`, no middleware) |

---

## API tests (Django REST Framework)

When the project uses **Django REST Framework** (DRF), use `rest_framework.test.APITestCase`
and `APIClient`, which add helpers for JSON serialisation and authentication tokens.

```python
# accounts/tests/test_api.py
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from accounts.tests.factories import CustomUserFactory


class UserListAPITest(APITestCase):

    def setUp(self):
        self.admin = CustomUserFactory(is_staff=True)
        self.client.force_authenticate(user=self.admin)
        self.url = reverse("user-list")  # adjust to actual router URL name

    def test_list_returns_200(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_unauthenticated_request_returns_401(self):
        self.client.force_authenticate(user=None)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_user_returns_201(self):
        payload = {
            "username": "dave",
            "email": "dave@example.com",
            "password": "NewPass99!",
        }
        response = self.client.post(self.url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
```

### Tools / libraries

| Tool | Role |
|---|---|
| `rest_framework.test.APITestCase` | DRF-aware base class |
| `rest_framework.test.APIClient` | Client with `force_authenticate`, `credentials` helpers |
| `drf-spectacular` / `drf-yasg` | OpenAPI schema generation; can be validated in tests |

---

## Database / query tests

These tests verify ORM behaviour that goes beyond a single model method:
queries, managers, signals, constraints, and transactions.
Use `TransactionTestCase` when you need to test behaviour that spans
transaction boundaries (e.g. `IntegrityError` handling), because
`TestCase` wraps everything in a savepoint.

```python
# accounts/tests/test_db.py
from django.test import TestCase, TransactionTestCase
from django.db.utils import IntegrityError
from accounts.models import CustomUser


class CustomUserQueryTest(TestCase):

    def test_manager_filters_active_users(self):
        CustomUser.objects.create_user(
            username="active_user", email="a@example.com", password="P@ss1"
        )
        inactive = CustomUser.objects.create_user(
            username="inactive_user", email="b@example.com", password="P@ss1"
        )
        inactive.is_active = False
        inactive.save()

        active_users = CustomUser.objects.filter(is_active=True)
        self.assertEqual(active_users.count(), 1)


class UniqueConstraintTest(TransactionTestCase):

    def test_duplicate_username_raises_integrity_error(self):
        CustomUser.objects.create_user(
            username="dup", email="dup1@example.com", password="P@ss1"
        )
        with self.assertRaises(IntegrityError):
            CustomUser.objects.create_user(
                username="dup", email="dup2@example.com", password="P@ss1"
            )
```

### Tools / libraries

| Tool | Role |
|---|---|
| `django.test.TestCase` | Fast; wraps in a transaction (no real commit) |
| `django.test.TransactionTestCase` | Slower; allows testing actual commits / rollbacks |
| `django.test.LiveServerTestCase` | Starts a real HTTP server; needed for Selenium |
| `pytest-django` | `db`, `django_db_reset_sequences`, `transactional_db` fixtures |

---

## Browser / end-to-end tests

End-to-end (E2E) tests drive a real browser to interact with the running
application and verify complete user workflows.

```python
# e2e/test_login_flow.py  (example with Playwright)
from playwright.sync_api import sync_playwright
from django.test import LiveServerTestCase


class LoginFlowE2ETest(LiveServerTestCase):

    def test_user_can_log_in(self):
        with sync_playwright() as p:
            browser = p.chromium.launch()
            page = browser.new_page()
            page.goto(f"{self.live_server_url}/login/")
            page.fill('input[name="username"]', "alice")
            page.fill('input[name="password"]', "Pass1234!")
            page.click('button[type="submit"]')
            page.wait_for_url(f"{self.live_server_url}/")
            self.assertIn("Welcome", page.content())
            browser.close()
```

### Tools / libraries

| Tool | Role |
|---|---|
| `Selenium` + `selenium` (pip) | Classic browser automation; works with `LiveServerTestCase` |
| `Playwright` + `pytest-playwright` | Modern alternative to Selenium; faster and more reliable |
| `django.test.LiveServerTestCase` | Spins up a real WSGI server on a free port for browser tests |
| `splinter` | High-level wrapper around Selenium / WebDriver |

---

## Performance / load tests

Load tests measure how the application behaves under concurrent traffic.
They are typically run outside the Django test suite.

```python
# locustfile.py
from locust import HttpUser, task, between


class AnonymousUser(HttpUser):
    wait_time = between(1, 3)

    @task
    def view_home(self):
        self.client.get("/")

    @task(3)
    def view_recipe_list(self):
        self.client.get("/api/recipes/")
```

Run with:

```bash
locust -f locustfile.py --host=http://localhost:8000
```

### Tools / libraries

| Tool | Role |
|---|---|
| `Locust` | Python-based load testing framework |
| `k6` | JavaScript-based; integrates well with CI/CD |
| `Apache JMeter` | GUI-based; widely used in enterprise settings |
| `django-silk` | Profiling middleware for identifying slow queries / views |

---

## Security tests

Security tests verify that the application correctly enforces authentication,
authorisation, and input sanitisation.

```python
# accounts/tests/test_security.py
from django.test import TestCase
from django.urls import reverse
from accounts.tests.factories import CustomUserFactory


class PermissionTest(TestCase):

    def test_unauthenticated_user_cannot_access_profile(self):
        url = reverse("profile-detail", kwargs={"pk": "profile-uuid"})
        response = self.client.get(url)
        # expect a redirect to login or a 401/403
        self.assertIn(response.status_code, [302, 401, 403])

    def test_user_cannot_access_another_users_profile(self):
        owner = CustomUserFactory()
        other = CustomUserFactory()
        self.client.force_login(other)
        url = reverse("profile-detail", kwargs={"pk": owner.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)
```

### Tools / libraries

| Tool | Role |
|---|---|
| `django.test.Client` | Sufficient for auth / permission checks |
| `Bandit` | Static analysis for common security issues in Python code |
| `Safety` / `pip-audit` | Checks dependencies for known CVEs |
| `OWASP ZAP` | Dynamic application security testing (DAST) scanner |

---

## Measuring test coverage

```bash
# install
uv add --dev coverage pytest-cov

# run with coverage
uv run coverage run manage.py test
uv run coverage report -m          # text summary
uv run coverage html                # HTML report in htmlcov/
```

Or with `pytest-django`:

```bash
uv run pytest --cov=. --cov-report=html
```

---

## Recommended project structure

```
back-end/
└── accounts/
    ├── tests/
    │   ├── __init__.py
    │   ├── factories.py          # factory_boy factories
    │   ├── test_models.py        # unit tests for models
    │   ├── test_validators.py    # unit tests for validators / utils
    │   ├── test_forms.py         # unit tests for forms
    │   ├── test_views.py         # integration tests for views
    │   ├── test_api.py           # API endpoint tests (DRF)
    │   └── test_security.py      # permission / auth tests
    └── ...
```

---

## References

[^django-testing]: Django documentation – Testing
    [docs.djangoproject.com/en/stable/topics/testing/](https://docs.djangoproject.com/en/stable/topics/testing/)

[^django-test-tools]: Django documentation – Testing tools
    [docs.djangoproject.com/en/stable/topics/testing/tools/](https://docs.djangoproject.com/en/stable/topics/testing/tools/)

[^drf-testing]: Django REST Framework – Testing
    [www.django-rest-framework.org/api-guide/testing/](https://www.django-rest-framework.org/api-guide/testing/)

[^factory-boy]: factory_boy documentation
    [factoryboy.readthedocs.io/en/stable/](https://factoryboy.readthedocs.io/en/stable/)

[^pytest-django]: pytest-django documentation
    [pytest-django.readthedocs.io/en/latest/](https://pytest-django.readthedocs.io/en/latest/)

[^coverage]: coverage.py documentation
    [coverage.readthedocs.io/en/latest/](https://coverage.readthedocs.io/en/latest/)

[^playwright]: Playwright for Python documentation
    [playwright.dev/python/](https://playwright.dev/python/)

[^locust]: Locust documentation
    [docs.locust.io/en/stable/](https://docs.locust.io/en/stable/)
