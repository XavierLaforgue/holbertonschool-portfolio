import { BrowserRouter, Routes, Route } from 'react-router-dom';
import HomePage from './pages/HomePage';
import SignupPage from './pages/SignupPage';
// import LoginForm from './components/LoginForm';
// import AboutPage from './components/AboutPage';
import Header from './components/Header'
import Footer from './Footer'
import AuthProvider from './context/AuthContext';


function App() {
  return (
    <AuthProvider>
      <BrowserRouter>
        <Header/>
          <Routes>
            <Route path='/' element={<HomePage/>} />
            <Route path='/signup' element={<SignupPage/>} />
            {/* <Route path='/login' element={<LoginForm/>} />
            <Route path='/about' element={<AboutPage/>} /> */}
        </Routes>
        <Footer/>
      </BrowserRouter>
    </AuthProvider>
  )
}

export default App
