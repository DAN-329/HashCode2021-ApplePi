import addConnection from './addConnection';
import addMindMapNode from './addMindMapNode';
import colors from './colors';
import data from '../Data/data.json';
import initializeScene from './InitializeScene';
import calculateLevel1Coordinates from './calculateLevel1Coordinates';
import calculateLevel2Coordinates from './calculateLevel2Coordinates';


export default async function renderMindMap(div) {
  const { scene, renderer, camera } = initializeScene(div);

  console.log(typeof data)  

  console.log(data)
  console.log(data[1]["id"])


  var res=[]
  var i
  for(i=1;i<=Object.keys(data).length;i++)
  {
    if (data[String(i)]["id"] ==1){
      console.log("True")
      res.push({"id":data[String(i)]["id"] ,"label":data[String(i)]["label"]});
    }
    else{
      console.log("False")
      res.push({"id":data[String(i)]["id"] ,"label":data[String(i)]["label"],"parent":data[String(i)]["parent"]})
    } 
  }
  console.log("Res value is -",res);

  console.log(res)
  console.log("Data should have been updated")  
  const root = res.find((node) => node.parent === undefined);
  const level1 = res.filter((node) => node.parent === root.id);
  root.x = 0;
  root.y = 0;
  root.level = 0;

  await addMindMapNode(scene, root);
  const radius = 2;
  for (let level1index = 0; level1index < level1.length; level1index++) {
    const { x, y, angle } = calculateLevel1Coordinates({
      numberOfNodes: level1.length,
      parent: root,
      radius,
      index: level1index
    });
    const level1node = { ...level1[level1index], x, y, level: 1, angle };
    await addMindMapNode(scene, level1node);
    addConnection(scene, {
      color: colors.magenta,
      parentNode: root,
      childNode: level1node
    });
    const level2 = res.filter((node) => node.parent === level1node.id);
    for (let level2index = 0; level2index < level2.length; level2index++) {
      const { x: x2, y: y2 } = calculateLevel2Coordinates({
        numberOfNodes: level2.length,
        parent: level1node,
        radius,
        index: level2index
      });
      const level2node = { ...level2[level2index], x: x2, y: y2, level: 2 };
      await addMindMapNode(scene, level2node);
      addConnection(scene, {
        color: colors.violet,
        parentNode: level1node,
        childNode: level2node
      });
    }
  }
  renderer.render(scene, camera);
}
