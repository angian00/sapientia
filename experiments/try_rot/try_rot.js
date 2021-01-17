
const w = 100;
const h = 40;
const w2 = 18;
const h2 = 10;
const w1 = w - w2;
const h1 = h - h2;


let fgColor = "rgb(240, 214, 195)";
let bgColor = "rgb(35, 20, 10)";


let display;


function init() {
	display = new ROT.Display({
		width: w,
		height: h,
		fontFamily: "menlo",
		fontSize: 20,
		forceSquareRatio: false,
		fg: fgColor,
		bg: bgColor,
	});

	print_frame(w1, h1, 0, 0, title="Map");
	print_frame(w2, h1, w1, 0, title="Stats");
	print_frame(w, h2, 0, h1, title="Messages");

	document.body.appendChild(display.getContainer());
}


function print_frame(w, h, x=0, y=0, title=null) {
	display.draw(x, y, "\u2552");
	display.drawText(x+1, y, "\u2550".repeat(w-2));
	display.draw(x+w-1, y, "\u2555");
	
	for (let i=1; i < h-1; i++) {
		display.draw(x, y+i, "\u2502");
		display.draw(x+w-1, y+i, "\u2502");
	}

	display.draw(x, y+h-1, "\u2514");
	display.drawText(x+1, y+h-1, "\u2500".repeat(w-2));
	display.draw(x+w-1, y+h-1, "\u2518");

	if (title) {
		//rot.js drawText trims spaces before printing

		//display.drawText(x+2, y, ` ${title} `);
		display.draw(x+2, y, " ");
		display.drawText(x+3, y, title);
		display.draw(x+2 + title.length + 1, y, " ");		
	}
}


init();
