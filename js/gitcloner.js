const cmd = require('node-cmd')
const fetch = require('node-fetch')
const config = require( "/home/pi/projects/rpi_tools/config.json" ).gitcloner

let modules = {}
let daemons = []


console.log(config);

class GitModuleUpdateDaemon {
	constructor (s_url, f_update_interval) {
		this.s_url = s_url;
		this.i_interval_id = setInterval(()=>{
			this.check()
		}, f_update_interval)
		
		this.check()
	}
	
	check(){
		fetch(this.convert_gitclone_url(this.s_url)).then((r)=>{
			return r.json()
		}).then((r)=>{
			console.log(r)
		})
		
	}
	
	kill(){
		clearInterval(this.i_interval_id)
	}
	
	convert_gitclone_url(s_url){
		let result = s_url;
		result = result.split(".git")[0]
		result = result.split("github.com")[1]
		
		return `https://raw.githubusercontent.com${result}/master/package.json`
	}
}



let list_repo_daemon = new GitModuleUpdateDaemon(config.list_repo, config.list_update_interval)
