// import { useState } from 'react'
import './App.css'
import Header from './Header'
import HeroCarousel from './HeroCarousel'
import SiteManual from './SiteManual'
import Footer from './Footer'

function App() {
  // const [count, setCount] = useState(0)

  return (
    <>
      <Header />
      <main className="main-content">
        <HeroCarousel />
        <SiteManual />
      </main>
      <Footer />
    </>
  )
}

export default App
