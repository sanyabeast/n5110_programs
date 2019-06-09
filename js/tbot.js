const TelegramBot = require( "node-telegram-bot-api" );
const request = require( "request" )
const config = require( "../config.json" )
const { exec } = require( "child_process" );

const TOKEN = config.tbot.token;
const bot = new TelegramBot( TOKEN, { polling: true });

bot.onText( /\/r (.+)/, async ( msg, match ) => {
	if ( config.tbot.authorized.indexOf( msg.chat.username ) > -1 ) {
		let command = match[ 1 ]
		
		exec( command, ( err, stdout, stderr )=>{
			bot.sendMessage( msg.chat.id, stdout );
		} )
		
	}
});

bot.onText(/Hi/, function onAudioText(msg) {
	bot.sendAudio(msg.chat.id, "Hi!" );
});


