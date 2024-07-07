import SigninForm from "../apis/SigninForm";
import SignupForm from "../apis/SignupForm";
import Destination from "../component/Pages/Destination";
import Home from "../component/Pages/Home";

export const routers = [
  {
    path: '/',
    element: <Home />,
    children: [
      {
        path: '/signin',
        element: (
            <SigninForm />
        ),
      },
      {
        path: '/singup',
        element: (
            <SignupForm />
        ),
      },
      {
        path: '/destination',
        element: (
            <Destination />
        ),
      }
    ],
  },
];