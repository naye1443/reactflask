import React, {useState} from "react"
import { useNavigate } from "react-router-dom"
import "../../Style/Login-Registration.css"

const Registration = () => {
    const navigate = useNavigate()
    let [email, set_email] = useState("")
    let [password, set_password] = useState("")
    let [first_name, set_first_name] = useState("")
    let [last_name, set_last_name] = useState("")

    let register_account = async (e) => {
        let formData = new FormData()
        formData.append('email', email)
        formData.append('password', password)
        formData.append('first_name', first_name)
        formData.append('last_name', last_name)

        const response = await fetch('/register', {
            method: 'POST',
            mode: 'cors',
            body: formData
        })
        .then(x => x.json())

        console.log(response)

        if(response === "success") {
            console.log("Successfully created account")
            localStorage.setItem("email", email)
            localStorage.setItem("logged_in", "true")

            navigate("/home")
        }
        else {
            console.log("create failed")
        }
    }

    return(
        <div className="login-form">
            <h1>CREATE ACCOUNT</h1>

            <form>
                <div className="content">
                    <div className="input-field">
                        <input type="email" placeholder="Email" autoComplete="nope" onChange={(e) => {
                            set_email(e.target.value)}}/>
                    </div>

                    <div className="input-field">
                        <input type="password" placeholder="Password" autoComplete="new-password" onChange={(e) => {
                            set_password(e.target.value)}}/>
                    </div>

                    <div className="input-field">
                        <input type="first_name" placeholder="First Name" autoComplete="first" onChange={(e) => {
                            set_first_name(e.target.value)}}/>
                    </div>

                    <div className="input-field">
                        <input type="last_name" placeholder="Last Name" autoComplete="last" onChange={(e) => {
                            set_last_name(e.target.value)}}/>
                    </div>
                </div>

                <div className="action">
                    <button type="button" onClick={() => navigate("/")}>Return</button>
                    <button type="button" onClick={() => register_account()}>Create</button>
                </div>

            </form>
        </div>
    );
}
export default Registration;

