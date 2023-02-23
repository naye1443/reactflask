import {BrowserRouter, Routes, Route} from "react-router-dom";
import {Home} from "../Pages/Home";
import {Images} from "../Pages/Images";
function AppRouter() {

    return (

        <BrowserRouter>
            <Routes>
                
                <Route path="/" element={
                    <Home/>
                }/>

                <Route path="/images" element={
                    <Images/>
                }/>
                
            </Routes>
        </BrowserRouter>

    )
}
export default AppRouter;