import "../../Style/Home.css"
import {useEffect, useState} from "react";
import ImageList from "./ImageList";

const Home = () => {
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
    };

    return (
        <div>
            <h2 className="list-title">Images</h2>
            <ImageList/>
        </div>
        
    );
}
export default Home;
