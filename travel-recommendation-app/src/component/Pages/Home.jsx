// import { Link, Outlet } from "react-router-dom"

import { Link, Outlet } from "react-router-dom"
// import Navagation from "../Layout/Navagation"

const Home = () => {
  return (

    <>
      {/* <div className="w-full h-screen relative">
        <img
          src="bg2.jpg"
          alt=""
          className="w-full h-full object-cover"
        />
      </div>
      <div>
        <Navagation />
      </div> */}
      <Link to="/signin"><div className="text-red">7</div></Link>
      <Outlet />
    </>
  )
}

export default Home