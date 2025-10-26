import { BrowserRouter, Routes, Route } from 'react-router-dom';
import HomePage from './pages/HomePage';
import SignupPage from './pages/SignupPage';
import LoginPage from './pages/LoginPage';
import UpdateRecipePage from './pages/UpdateRecipePage';
// import AboutPage from './components/AboutPage';
import Header from './components/Header'
import Footer from './Footer'
import AuthProvider from './context/AuthProvider';
import UpdateProfilePage from './pages/UpdateProfilePage';


function App() {
  return (
    <AuthProvider>
      <BrowserRouter>
        <Header/>
          <Routes>
            <Route path='/' element={<HomePage/>} />
            <Route path='/signup' element={<SignupPage/>} />
            <Route path='/login' element={<LoginPage/>} />
            <Route path='/profile/update' element={<UpdateProfilePage/>} />
            <Route path='/recipe/update/:recipeId' element={<UpdateRecipePage/>} />
            {/* <Route path='/recipes' element={<RecipesPage/>} /> */}
            <Route path='/about' element={<HomePage/>} />
        </Routes>
        <Footer/>
      </BrowserRouter>
    </AuthProvider>
  )
}

export default App
