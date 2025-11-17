import React from "react";
import "../css/LeftPanel.css";
import DashboardIcon from "../images/Dashboard.png";
import CustomRatingIcon from "../images/CustomRating.png";
import ReportsIcon from "../images/Reports.png";
import SystemDescriptionIcon from "../images/SystemDescription.png";
import HelpFeetbackIcon from "../images/HelpFeetback.png";
import { NavLink, useLocation } from "react-router-dom";



const pageNames = {
    "/": "Dashboard",
    "/customrating": "Custom Rating",
    "/reports": "Reports",
    "/systemdescription": "System Description",
    "/help": "Help & Feedback",
};



function LeftPanel() {
    const location = useLocation();
    const CurrentPageName = pageNames[location.pathname] || "Dashboard";
    return (
        <div className="LeftPanel">
            <div className="CurrentPage">
                <div className="text">{CurrentPageName}</div>
            </div>

            {/* AnalyticsHub */}
            <div className="AnalyticsHub">
                <div className="text">Analytics Hub</div>

                <div className="nav-item">
                    <img src={DashboardIcon} alt="Dashboard" />
                    <NavLink to="/" end className={({ isActive }) => `nav-link ${isActive ? "active" : ""}`}>
                        Dashboard
                    </NavLink>
                </div>

                <div className="nav-item">
                    <img src={CustomRatingIcon} alt="Custom Rating" />
                    <NavLink to="/customrating" className={({ isActive }) => `nav-link ${isActive ? "active" : ""}`}>
                        Custom Rating
                    </NavLink>
                </div>

                <div className="nav-item">
                    <img src={ReportsIcon} alt="Reports" />
                    <NavLink to="/reports" className={({ isActive }) => `nav-link ${isActive ? "active" : ""}`}>
                        Reports
                    </NavLink>
                </div>
            </div>

            {/* Useful Information */}
            <div className="UsefulInformation">
                <div className="text">Useful Information</div>

                <div className="nav-item">
                    <img src={SystemDescriptionIcon} alt="System description" />
                    <NavLink to="/systemdescription" className={({ isActive }) => `nav-link ${isActive ? "active" : ""}`}>
                        System description
                    </NavLink>
                </div>

                <div className="nav-item">
                    <img src={HelpFeetbackIcon} alt="Help & Feedback" />
                    <NavLink to="/help" className={({ isActive }) => `nav-link ${isActive ? "active" : ""}`}>
                        Help & Feedback
                    </NavLink>
                </div>
            </div>
        </div>
    );
}

export default LeftPanel;
