import {BrowserRouter, Routes, Route} from "react-router-dom";
import Home from "../Pages/Home";
import Login from "../Pages/Login";
import Registration from "../Pages/Registration";

function AppRouter() {
    return (
        <BrowserRouter>
            <Routes>
                
                <Route path="/" element={
                    <Login/>
                }/>

                <Route path="/register" element={
                    <Registration/>
                }/>

                <Route path="/home" element={
                    <Home/>
                }/>

            </Routes>
        </BrowserRouter>
    )
}
export default AppRouter;