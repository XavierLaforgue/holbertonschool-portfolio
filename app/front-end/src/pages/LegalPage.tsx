/**
 * Legal notice and privacy policy (RGPD).
 *
 * The legal notice says who publishes and who hosts the site (French law
 * "LCEN", article 6). The privacy policy tells users what personal data
 * the application keeps, why, for how long, and how to exercise their
 * rights (RGPD, articles 13 to 21).
 */

// The address users write to for any question about their data.
const CONTACT_EMAIL = 'xavier.laforgue@holbertonstudents.com'

const h2Class = 'mt-8 mb-2 text-lg font-semibold'
const listClass = 'list-disc space-y-1 pl-5'

export default function LegalPage() {
	return (
		<section className="mx-auto max-w-3xl px-4 py-12 text-sm leading-relaxed">
			<h1 className="mb-6 text-2xl font-bold">Legal notice and privacy</h1>

			<h2 className={h2Class}>Legal notice</h2>
			<ul className={listClass}>
				<li>
					<strong>Publisher and publication director:</strong> Xavier
					Laforgue, private individual. animize_eat is a personal,
					non-commercial project made at Holberton School (Dijon).
				</li>
				<li>
					<strong>Contact:</strong>{' '}
					<a href={`mailto:${CONTACT_EMAIL}`} className="underline">
						{CONTACT_EMAIL}
					</a>
				</li>
				<li>
					<strong>Hosting:</strong> the application is not online yet:
					it runs on the publisher's computer for demonstrations. The
					name, address and phone number of the host will be given here
					when it goes online.
				</li>
			</ul>

			<h2 className={h2Class}>Personal data we keep</h2>
			<ul className={listClass}>
				<li>
					your email address and your password, which is stored only
					in a hashed form: nobody, not even the administrator, can
					read it;
				</li>
				<li>
					your display name (generated automatically when you sign up)
					and the optional details of your profile, which the
					interface does not ask for today;
				</li>
				<li>
					the recipes and photos you write. When you publish a recipe,
					every visitor can see it, with your display name.
				</li>
			</ul>
			<p className="mt-2">
				Sign-up asks only for your email address and a password.
			</p>

			<h2 className={h2Class}>Why, and on what legal basis</h2>
			<p>
				This data is used only to run your account and to let you
				write, publish and save recipes: it is needed to provide the
				service you asked for when you signed up (RGPD, article
				6.1.b). It is never sold or shared: nobody else receives it.
			</p>

			<h2 className={h2Class}>How long</h2>
			<p>
				As long as your account exists. "Delete my account", on the
				"My account" page, immediately deletes your account, your
				profile, your recipes and their photos. Copies of your published
				recipes that other members saved stay in their account, without your name.
			</p>

			<h2 className={h2Class}>Your rights</h2>
			<p>
				You can access, correct and delete your data, ask us to limit
				its use or object to it, and receive it in a reusable format
				(RGPD, articles 15 to 21). Delete your account yourself from the
				"My account" page; for anything else, write to{' '}
				<a href={`mailto:${CONTACT_EMAIL}`} className="underline">
					{CONTACT_EMAIL}
				</a>
				: you will get an answer within one month. If you think your
				rights are not respected, you can complain to the CNIL (
				<a href="https://www.cnil.fr/fr/plaintes" className="underline">
					cnil.fr/fr/plaintes
				</a>
				).
			</p>

			<h2 className={h2Class}>Cookies and browser storage</h2>
			<ul className={listClass}>
				<li>
					<code>access_token</code> (5 minutes) and{' '}
					<code>refresh_token</code> (1 day): they keep you logged in.
					They are HttpOnly: the page's JavaScript cannot read them.
				</li>
				<li>
					<code>theme</code>, kept in your browser (localStorage): your
					choice of light or dark theme.
				</li>
			</ul>
			<p className="mt-2">
				They are strictly necessary for the service, and the site uses no
				audience measurement, no advertising and no third-party
				cookies: that is why no consent banner is needed.
			</p>
		</section>
	)
}
