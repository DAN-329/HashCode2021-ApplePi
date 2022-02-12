import React from "react";
import { NavLink as Link } from 'react-router-dom';
import {BrowserRouter as Router, Route,Routes} from 'react-router-dom';
import styled from 'styled-components';
import wordie from '../images/WordieIcon.png';


export const Nav = styled.nav`
  background: white;
  height: 80px;
  display: flex;
  justify-content: space-around ;
  // justify-content: space-between ;
  padding: 5px;
`;

export const NavLink = styled(Link)`
  color:black;
  display: flex;
  font-size:22px;
  font-weight: 600;
  align-items: center;
  text-decoration: none;
  padding: 0 1.3rem;
  cursor: pointer;
  &.active {
    color: #1aa3ff;
  }
`;


export const NavMenu = styled.div`
  padding-top:60px;
  display: flex;
  align-items: center;
  // margin-right: -24px;
  @media screen and (max-width: 768px) {
    display: none;
  }
`;

function Menu(){
    return(
        <div>
  
            <div ClassName="Container">
              {/* <Router> */}
                <Nav>
                  
                  <Link to='/'> 
                    <img src={wordie} className="wordieMenu"></img>
                  </Link>
                  
                  <NavLink to='/'>
                    
                    <div class="MenuFlex">
                      
                      <br></br>
                      <div className="Header">
                        Wordie
                      </div>
                    </div>
            
                  </NavLink>

                    <NavMenu>
                      <NavLink to="/MindMap" activeStyle className="Navlinks">
                        Mind Map
                      </NavLink >
                      {/* <NavLink to='/s' activeStyle className="Navlinks">
                        History
                      </NavLink > */}
                    </NavMenu>
              
              </Nav>
            {/* </Router> */}
      </div>
        </div>
    );
};

export default Menu;