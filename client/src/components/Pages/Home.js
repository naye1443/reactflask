import "../../Style/Home.css"
import { useNavigate } from "react-router-dom"
import {useEffect, useState} from "react";
import ImageList from "./ImageList";

const Home = () => {
    const navigate = useNavigate()

    useEffect(() => {
        createImageList();
    }, []);
    
    const createImageList = () => {
        let userName = '';
        return (
            <ImageList
                userName = {userName}
            />
        )
    }

    const logout = () => {
        localStorage.setItem("email", "")
        localStorage.setItem("logged_in", "false")
        navigate("/")
    }



    return (
        <div>
            <h2 className="list-title">Images</h2>
            <ImageList/>

            <div>
                <button onClick={() => logout()}>LOGOUT</button>
            </div>
        </div>
        
    );
}
export default Home;
