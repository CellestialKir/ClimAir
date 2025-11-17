import React from "react";
import '../css/Header.css'
import Logo from '../images/Logo.png'
import UserLogo from '../images/UserLogo.png'
import LightMod from '../images/LightMod.png'
import DarkMod from '../images/DarkMod.png'


function Header() {
    return (
        <>
            <div className="header">
                <div className="Logo_container">
                    <img src={Logo} alt="Logo" className="Logo" />
                </div>

                <div className="Button_container">
                    <div className="SwitchTheme">
                        <div className="Light">
                            <img src={LightMod} alt="light mode" />
                        </div>
                        <div className="Dark">
                            <img src={DarkMod} alt="Dark mod" />
                        </div>
                    </div>

                    <div className="District">
                        <div className="text"> Medeu District ∨ </div>
                    </div>

                    <div className="User">
                        <img src={UserLogo} alt="UserLogo" className="UserLogo" />
                    </div>

                </div>
            </div>
        </>
    )
}

export default Header;