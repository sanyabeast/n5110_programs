#! /usr/bin/env node

const { exec } = require( "child_process" );
const username = process.argv[ 2 ]
const config = require( `/home/${ username }/.config/autostart.json` )

config.commands.forEach( ( command )=>{
	exec( command, log )
})

function log ( err, stdout, stderr ) {
	console.log( err, stdout, stderr )
}