#! /usr/bin/env node

const { exec, spawn } = require( "child_process" );
const username = process.argv[ 2 ]
const config = require( `/home/${ username }/.config/autostart.json` )

for ( var a = 0; a < config.commands.length; a++){
	let cc = config.commands.length 
	let sq = Math.ceil(Math.sqrt(config.commands.length))
	let x = (a % sq) * 1920 / sq
	let y = Math.floor( a / sq ) * 1080 / sq
	let w = 300 / sq
	let h = 70 / sq
	
	desktop = 1
	
	let command = config.commands[a]
	if ( typeof command === "string" ){
			set_desktop(desktop)
			exec( `xterm -hold -geometry ${w}x${h}+${x}+${y} -e "${ command }"`, log )
	} else {
		log(command)
			params = {
					title: `autostart: ${ command.run }`,
					...command
			}
			
			if (params.desktop !== undefined){
				desktop = params.desktop
			}
			
			
			if (params.align !== undefined ){
				console.log(1111)
				g = get_geometry(params.align)
				x = g.x
				y = g.y
				w = g.w
				h = g.h
			}
			
			set_desktop(desktop)
			
			exec( `xterm -hold -name "${ params.title }" -geometry ${w}x${h}+${x}+${y} -e "${ command.run } "`, log )
	}
	
	lock(1.5)
} 

set_desktop(0)

function get_geometry(align){
		vw = 300
		vh = 70
		sw = 1920
		sh = 1080
		x = 0
		y = 0
		w = 100
		h = 100
		
		switch(align){
				case "top-left":
					x = 0; y = 0; w = vw / 2; h = vh / 2; break;
				case "top-right":
					x = sw / 2; y = 0; w = vw / 2; h = vh / 2; break;
				case "bottom-left":
					x = 0; y = sh/2; w = vw / 2; h = vh / 2; break;
				case "bottom-right":
					x = sw/2; y = sh/2; w = vw / 2; h = vh / 2; break;
				case "top":
					x = 0; y = 0; w = vw; h = vh/2; break;
				case "bottom":
					x = 0; y = sh/2; w = vw; h = vh/2; break;
				case "left":
					x = 0; y = 0; w = vw/2; h = vh; break;
				case "right":
					x = sw/2; y = 0; w = vw/2; h = vh; break;
				case "full":
					x = 0; y = 0; w = vw; h = vh; break;
		}
		
		console.log("geom", x, y, w, h)
		
		return {
				x, y, w, h
		}
}

function lock(duration){
	now = +new Date()
	end = now + duration * 1000
	while(+new Date() < end){}
}

function set_desktop(id){
	exec( `xdotool set_desktop ${id}`, log )
}

function log ( err, stdout, stderr ) {
	console.log( err, stdout, stderr )
}
