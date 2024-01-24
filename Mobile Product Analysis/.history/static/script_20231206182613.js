jQuery(document).ready(function ($) {
	jQuery(document).on("click", ".iconInner", function (e) {
		jQuery(this).parents(".botIcon").addClass("showBotSubject");
		$("[name='msg']").focus();
	});

	jQuery(document).on("click", ".closeBtn, .chat_close_icon", function (e) {
		jQuery(this).parents(".botIcon").removeClass("showBotSubject");
		jQuery(this).parents(".botIcon").removeClass("showMessenger");
	});

	jQuery(document).on("submit", "#botSubject", function (e) {
		e.preventDefault();

		jQuery(this).parents(".botIcon").removeClass("showBotSubject");
		jQuery(this).parents(".botIcon").addClass("showMessenger");
	});

	/* Chatboat Code */
	$(document).on("submit", "#messenger", function (e) {
		e.preventDefault();

		var val = $("[name=msg]").val().toLowerCase();
		var mainval = $("[name=msg]").val();
		name = "";
		nowtime = new Date();
		nowhoue = nowtime.getHours();

		function userMsg(msg) {
			$(".Messages_list").append(
				'<div class="msg user"><span class="avtr"><figure style="background-image: url(https://mrseankumar25.github.io/Sandeep-Kumar-Frontend-Developer-UI-Specialist/images/avatar.png)"></figure></span><span class="responsText">' +
					mainval +
					"</span></div>"
			);
		}
		function appendMsg(msg) {
			$(".Messages_list").append(
				'<div class="msg"><span class="avtr"><figure style="background-image: url(https://mrseankumar25.github.io/Sandeep-Kumar-Frontend-Developer-UI-Specialist/images/avatar.png)"></figure></span><span class="responsText">' +
					msg +
					"</span></div>"
			);
			$("[name='msg']").val("");
		}


        

        if (mainval.trim() === '') {
            appendMsg("Please enter a question.");
            return
        }else{
            userMsg(mainval);
        }

        fetch('/process', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            body: 'userInput=' + encodeURIComponent(mainval)
        })
        .then(response => response.json())
        .then(data => {
            // document.getElementById('botResponse').innerText = 'Bot: ' + ;
            appendMsg(data.response);
        })
        .catch(error => console.error('Error:', error));

		
		
        



       


		function saybye() {
			if (nowhoue <= 10) {
				appendMsg(" have nice day! :)");
			} else if (nowhoue >= 11 || nowhoue <= 20) {
				appendMsg(" bye!");
			} else {
				appendMsg(" good night!");
			}
		}

		var lastMsg = $(".Messages_list").find(".msg").last().offset().top;
		$(".Messages").animate({ scrollTop: lastMsg }, "slow");
	});
	/* Chatboat Code */
});
