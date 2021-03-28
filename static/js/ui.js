var getGameDesc = function(title) {
  var temp = "<p>\"Press <b>Start new game\"</b> to start the game!</p>";
  switch(title){
    case "qbert":
      return temp + "<p>With Q*bert, your goal is to score as many points as possible by changing the color of every cube in the pyramid into the pyramid's 'destination' color. To do so, you must hop onto each cube in the pyramid one at a time, while avoiding the nasty creatures that lurk there. These creatures want nothing more than to stop your progress.</p><p>Use <b>arrow keys</b> to control Q*bert.</p><p>More details in the <a href='https://atariage.com/manual_html_page.php?SoftwareLabelID=377' target='_blank'>original manual</a>.</p>";
    case "revenge":
      return temp + "<p>Help PANAMA JOE safely reach Montezuma’s fantastic treasure by guiding him through a maze of death-dealing chambers within the emperor’s fortress. Along the way, PANAMA JOE must avoid an array of deadly creatures while he collects valuables and tools which can aid him in mastering the evils of the fortress and eventually, escaping with the  loot!</p><b>Arrow keys</b> are for moving, <b>SPACE</b> is to jump.<p></p><p>More details in the <a href='https://atariage.com/manual_html_page.php?SoftwareLabelID=310' target='_blank'>original manual</a>.</p>";
    case "pinball":
      return temp + "<p>VIDEO PINBALL TM is a game of skill and chance. It is like the large arcade pinball games, complete with sounds and bright colors that set the mood for the ultimate VIDEO PINBALL challenge.</p>Use the <b>arrow keys</b> to move your flippers. Move the <b>right arrow</b> to move the right flipper up, and <b>left arrow</b> to move the left flipper up. Use the <b>upper arrow</b> to move both flippers at the same time. Use the <b>down arrow</b> to bring the plunger back. Press <b>SPACE</b> to release the spring and shoot the ball into the playfield</p><p>More details in the <a href='https://atariage.com/manual_html_page.php?SoftwareLabelID=588' target='_blank'>original manual</a>.</p>";
    case "spaceinvaders":
      return temp + "<p>Each time you turn on SPACE INVADERS you will be at war with enemies from space who are threatening the earth. Your objective is to destroy these invaders by firing your laser cannon. You must wipe out the invaders either before they reach the earth (bottom of the screen), or before they hit you three times with their laser bombs.</p><p>Use <b>arrows</b> for moving and <b>SPACE</b> key for firing.</p><p>More details in the <a href='https://atariage.com/manual_html_page.php?SoftwareLabelID=460' target='_blank'>original manual</a>.</p>";
    case "mspacman":
      return temp + "<p>Use <b>arrow keys</b> to control MS.PAC-MAN.</p><p>MS.PAC-MAN encounters floating fruit and pretzels while traveling around the maze. Gobble up these munchies, and you score bonus points. But watch out! Fearful ghosts scurry about trying to gobble up MS.PAC-MAN.</p><p>As soon as she gulps down the energy pill, the ghosts turn blue with fright and you can get points for eating them.</p><p>More details in the <a href='https://atariage.com/manual_html_page.php?SoftwareLabelID=320' target='_blank'>original manual</a>.</p>";
    case "seaquest":
      return temp + "<p>We need your help to teach an Atari agent how to maximize its score during the Seaquest game. <p>Each time you turn on SEAQUEST, you will be piloting a submarine in a sea filled with dangerous sea creatures. Your objective is to rescue the people in the water. Be careful to come up to refill your oxygen and avoid the enemy or the submarine will sink to the ocean floor!</p><p>Use <b>arrows</b> for moving and <b>SPACE</b> key for firing your torpedoes.</p><p>More details in the <a href='https://atariage.com/manual_html_page.php?SoftwareLabelID=424' target='_blank'>original manual</a>.</p></p>";
    case "enduro":
      return temp + "<p>We need your help to teach an Atari agent how to maximize its score during the Enduro game. <p>Each time you turn on ENDURO, you will be partaking in a competitive car race.  Your objective is to pass as many cars as you possibly can. Be careful not to crash into the other cars!</p><p>Use <b>arrows</b> for moving and <b>SPACE</b> key for accelerating.</p><p>More details in the <a href='https://atariage.com/manual_html_page.php?SoftwareLabelID=163' target='_blank'>original manual</a>.</p></p>";
  }
  return "";
}

var focus_console = function() {
  document.getElementById('javatari-screen').focus();
}

window.onload = function() {
  focus_console();
  document.getElementById("javatari-screen").addEventListener('blur', function(event) {
      setTimeout(function() {focus_console();}, 30);
  });
  //if (rom != "revenge" && rom != "qbert") {
	setup_reset_btn(document.getElementById("reset"));
  //}
  $("#game-desc").html(getGameDesc(rom));
  if(rom != '') {
  //if(rom != '' && rom != "revenge" && rom != "qbert") {
    load_rom(rom); 
  }

  if (typeof(Storage) !== "undefined") {
    if(localStorage.getItem("isMuted") == null || localStorage.getItem("isMuted") == "true") {
      //Javatari.room.speaker.mute();
      localStorage.setItem("isMuted", true);
      $("#sound-btn").addClass("off");
      $("#sound-btn").text("Sound OFF");
    } else {
      $("#sound-btn").addClass("on");
      $("#sound-btn").text("Sound ON");
    }
  }

  //$("#sound-btn").click(function(){
  //  if($(this).hasClass('off')) {
  //    $(this).text("Sound ON");
  //    $(this).removeClass('off').addClass('on');
  //    Javatari.room.speaker.play();
  //    localStorage.setItem("isMuted", "false");
  //    
  //  } else if($(this).hasClass('on')) {
  //    $(this).text("Sound OFF");
  //    $(this).removeClass('on').addClass('off');
  //    Javatari.room.speaker.mute();
  //    localStorage.setItem("isMuted", "true");
  //  }
  //});
  scores = 0;

}

window.onbeforeunload = function() {Javatari.room.console.save_seq();}; 

var load_rom = function(title) {
  Javatari.room.romLoader.loadFromURL(ROM_PATH + title + '.bin');
}

var setup_reset_btn = function(but) {
	control = jt.ConsoleControls.RESET;
	controlsSocket = Javatari.room.console.getControlsSocket();
	but.style.cursor = "pointer";
  var mouseDown;
  but.addEventListener("mousedown", async function (e) {
    //console.log(e);
    //save_the_event = e;
  if (e.preventDefault) e.preventDefault();
    //if (clicked == false) {
    //  load_rom(rom); 
    //}
    $("#reset").css("background-color", "green");
    $("#reset").html("Game has started");

    clicked = true;
    mouseDown = true;
    controlsSocket.controlStateChanged(control, true);
    await Javatari.room.console.resetEnv();
    //click_start = Date.now();
    //reset_stuff();
		controlsSocket.controlStateChanged(control, false);
	});
	but.addEventListener("mouseup", function (e) {
	if (e.preventDefault) e.preventDefault();
		mouseDown = false;
		//controlsSocket.controlStateChanged(control, false);
	});
	but.addEventListener("mouseleave", function (e) {
		if (e.preventDefault) e.preventDefault();
		if (!mouseDown) return;
		mouseDown = false;
		//controlsSocket.controlStateChanged(control, false);
	});
}

//var reset_stuff = async function() {
//	  control = jt.ConsoleControls.RESET;
//	  controlsSocket = Javatari.room.console.getControlsSocket();
//    controlsSocket.controlStateChanged(control, true);
//    await Javatari.room.console.resetEnv();
//    controlsSocket.controlStateChanged(control, false);  // i'm so stupid
//}

var update_score = function(text) {
    //var percentile = 100;
    //for(var i=99; i>=0;i--) {
    //  if(scores[i] > score) {
    //    percentile-=1;
    //  } else {
    //    break;
    //  }
    //}
    if (enable_ui == true) {
      $("#ai-bar-text").html(text);
    }
    //ai_percentile = parseInt(100*score/ai_score);
    //if(ai_percentile > 100) {
    //  ai_percentile = 100;
    //}
    //$("#ai-score").width(ai_percentile+"%");
}

