# Cartoon Shader for Blender

A simple Blender add-on that generates a cartoon-style material with adjustable shades, colors, and outlines.  
Works best on 3D objects with a higher face count.  

![Image](./media/3d_2.png)  
![Video](./media/3d_2.mp4)  

---

## Installation
1. Copy the add-on folder into:  
   `..../Blender/version/scripts/addons`  
2. In Blender, go to *Edit > Preferences > Add-ons* and enable **Cartoon Shader**.  

---

## Usage
1. Select an active object in the scene.  
2. In the 3D Viewport, press **N** → open the **Cartoon Shader Creator** tab.  
3. Set parameters (main color, number of shades, outline thickness).  
4. Click **Generate Cartoon Shader**.  

The add-on will create both the cartoon shader and a camera-based outline.  

---

## Features
- **Main Color** – base color of the material, used to generate all shades.  
- **Number of Shades** – controls the gradient steps for the cartoon effect.  
- **Outline Thickness** – defines the width of the outline drawn using **Grease Pencil Line Art**.  

**Shader Principle:**
- Built from **Principled BSDF**, **Shader to RGB**, **Color Ramp**, and **Material Output** nodes.  
- Constant interpolation in the Color Ramp ensures sharp shade transitions.  

---

## Development Notes
- Inspired by community tutorials and adapted into a user-friendly add-on.

References:  
- [Video 1](https://www.youtube.com/watch?v=8HHQUD3HxdY)  
- [Video 2](https://www.youtube.com/shorts/JLCs98lpR_Q)  
- [Video 3](https://www.youtube.com/watch?v=bViS42E8Y4M)  
- [Video 4](https://www.youtube.com/watch?v=NPZq_GYtx28)  

