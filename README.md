# Material Viewport Color from Nodes

## Where do I find it?

Once you have enabled the add-on in your preferences,
you can find its UI and operators in your object's material properties tab.

## Operators

There are multiple operators that you can use to set materials. You can limit its scope to:
- the active material
- the active object
- all selected objects
- all materials in the blend file

For the active material, you can also tell the add-on to evaluate your currently selected node
instead of from the output node.

## How does it work?
For a given material, the add-on starts at the output node
(or the currently selected node, if you choose the "selected node" operator).
From that node, it uses the node type, available node sockets, and a configuration
to determine which sockets to use to evaluate color, metallic, and roughness.
If there is a default value set for that socket, it uses that.
However, if that socket is connected to another node, the add-on traverses the path to the previous node.

Then the process repeats: check the node type and configuration, and evaluate its sockets.
Once it finds a set value, it ends the traversal and sets it.

## Supported Nodes

The "+" next to it can also retrieve a metallic value from the node.
The "*" next to it means the add-on can also retrieve a roughness value from the node.

Shader nodes:
 - principled +*
 - emission
 - toon *
 - anisotropic *
 - diffuse *
 - glass *
 - glossy *
 - hair
 - principled hair *
 - refraction *
 - subsurface scattering
 - translucent
 - velvet *

The following are miscellaneous nodes, supported across all three value types.
Note that most of these do not actually evaluate the node itself,
but just check specific node sockets for a set value.
For example, the mix node does not apply the actual blend type to the values -
it simply mixes the two values.

 - RGB
 - Value
 - Map Range
 - Separate color
 - Group node
 - Brightness/Contrast
 - Gamma
 - Hue/Saturation/Value
 - Invert
 - RGB Curve
 - Clamp
 - Image and environment textures
 - Shader to RGB
 - Mix

Don't see the node you want in here? If you feel this node would benefit other users as well, make your case in the GitHub issues tab!
