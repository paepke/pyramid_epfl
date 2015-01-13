Components explained
====================

The software-design of the EPFL-components was done with the following requirements in mind:

- Components consists of parts ("compoparts") that can be spread over a page and rendered/refreshed individually.
	e.g. A form has two parts: 
		1. The fields
		2. The buttons
	The fields will be rendered in a scrollable container centered in the screen, the buttons at the bottom of the screen outside the scrolling container.
	or e.g. A table has two parts:
		1. The scrolling grid
		2. The paginator
	Again the grid is rendered in the main part of the screen, the paginator at the bottom, or depending on the page-layout at the top of the grid.

- These "compoparts" are defined by the component-designer - by name and by template. The user can use these shipped parts or overwrite the template of each compopart. When overwriting the compoparts the original component also uses these overwritten parts.
	This thechnique is used e.g. for a panel-layout-container-component. The individual parts of this container (north, south, east, west, center) are predefined empty in the component definition and then overwritten with the actual content by the page template.

- All components are self-drawing. So a component can be used on a page without any additional html-template. The page can influence the layout of the components by overwriting compoparts. This consequently means that a complete page can be desinged without any additional template - by using components stacked inside container-components.

- The javascript of the component is handeled separatly from the HTML.

- When rendering a component, the special named compopart "main" is rendered.

 
