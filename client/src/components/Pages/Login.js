import {MDBCol, MDBContainer, MDBInput, MDBCheckbox, MDBBtn, MDBIcon, MDBCard, MDBCardBody, MDBRow} from 'mdb-react-ui-kit'
import React, {useState} from "react"
import { useNavigate } from "react-router-dom"
import "../../Style/Login-Registration.css"

const Login = () => {
    const navigate = useNavigate()
    localStorage.setItem("logged_in", "false")
    let [email, setEmail] = useState("")
    let [password, setPassword] = useState("")

    let authenticate_account = async (e) => {
        let formData = new FormData()
        formData.append('email', email)
        formData.append('password', password)

        let response = await fetch('/login', {
            method: 'POST',
            mode: 'cors',
            body: formData
        })
        .then( x => x.json())

        console.log(response)

        if (response === 'success'){
            console.log("login success")
            localStorage.setItem("email", email)
            localStorage.setItem("logged_in", "true")
            navigate("/home")
        }
        else {
            console.log("login failed")
        }

    }

    if(localStorage.getItem("logged_in") === "true") {
        navigate("/home")
    }
    else {
        return (
            <div className="login-form">
                <h1>LOGIN</h1>

                <form>
                    <div className="content">
                        <div className="input-field">
                            <input type="email" placeholder="Email" autoComplete="nope" onChange={(e) => {
                                setEmail(e.target.value)}}/>
                        </div>

                        <div className="input-field">
                            <input type="password" placeholder="Password" autoComplete="new-password" onChange={(e) => {
                                setPassword(e.target.value)}}/>
                        </div>
                    </div>

                    <div className="action">
                        <button type="button" onClick={() => navigate("/register")}>Register</button>
                        <button type="button" onClick={() => authenticate_account()}>Sign in</button>
                    </div>

                </form>
            </div>
        )
    }
};
export default Login;
