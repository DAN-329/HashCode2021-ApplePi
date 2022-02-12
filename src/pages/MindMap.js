import React from "react";
import Menu from "../components/Menu";
// Rewuire for generation of the mind maps
// import * as THREE from 'three';
// import { createRef, useEffect } from 'react';
import MindMapNode from "../components/MindMapNode";

import MindMapViwer from "../components/MindMapViewer";


var data=[
    { "id": 1, "label": "Interests" },
    { "id": 2, "label": "Music", "parent": 1 },
    { "id": 3, "label": "Graphic Design", "parent": 1 },
    { "id": 4, "label": "Coding", "parent": 1 },
    { "id": 5, "label": "Piano", "parent": 2 },
    { "id": 6, "label": "Electronic", "parent": 2 },
    { "id": 7, "label": "Procreate", "parent": 3 },
    { "id": 8, "label": "Adobe Illustrator", "parent": 3 },
    { "id": 9, "label": "Computer Graphics", "parent": 4 },
    { "id": 10, "label": "React", "parent": 4 },
    { "id": 11, "label": "Reason", "parent": 6 },
    { "id": 12, "label": "Ableton Live", "parent": 6 },
    { "id": 13, "label": "Three.js", "parent": 9 },
    { "id": 14, "label": "Phaser", "parent": 9 }
  ]


//   function MindMapView() {
//     const divRef = createRef();
//     useEffect(() => {
//         const scene = new THREE.Scene();
//         const camera = new THREE.PerspectiveCamera(
//             75,
//             window.innerWidth / window.innerHeight,
//             0.1,
//             1000
//         );
//         const renderer = new THREE.WebGLRenderer();
//         renderer.setSize(window.innerWidth, window.innerHeight);
//         divRef.current.appendChild(renderer.domElement);
//         const geometry = new THREE.BoxGeometry();
//         const material = new THREE.MeshBasicMaterial({ color: 0x00ff00 });
//         const cube = new THREE.Mesh(geometry, material);
//         scene.add(cube);
//         camera.position.z = 5;
//         function animate() {
//             requestAnimationFrame(animate);
//             cube.rotation.x += 0.01;
//             cube.rotation.y += 0.01;
//             renderer.render(scene, camera);
//         }
//         animate();
//     }, [divRef]);

function MindMap(){
    
    ////////////  Test

    //////////////////////////////////////////////////////


    return(
        <div>
            <Menu></Menu>
            <br></br>
            <br></br>
            <br></br>
            <br></br>
            <br></br>
            Below is a mind map
            <br></br>
            <br></br>
            <MindMapViwer></MindMapViwer>
            <br></br>
            <br></br>   
            <MindMapNode></MindMapNode>


        </div>    
    )
    

}

export default MindMap;