import { BrowserRouter, Routes, Route } from 'react-router-dom';
import HomePage from './pages/HomePage';
import SignupPage from './pages/SignupPage';
// import LoginForm from './components/LoginForm';
// import AboutPage from './components/AboutPage';
import Header from './components/Header'
import Footer from './Footer'


function App() {
  return (
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
  )
}

export default App
