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

	let scrollTop      = 0
	let easedScrollTop = 0
	let $content       = document.querySelector('.js-content')
	let $fakeScroll    = document.querySelector('.js-fake-scroll')

	document.addEventListener('scroll', ()=>{
		scrollTop = window.pageYOffset || document.documentElement.scrollTop
	})

	function resize() {
		$fakeScroll.style.height = $content.clientHeight + 'px'
	}

	window.addEventListener('resize', resize)

	function update() {
		requestAnimationFrame( update )
		easedScrollTop += (scrollTop - easedScrollTop) * 0.1
		$content.style.transform = 'translateY('+ (easedScrollTop * -1) +'px) translateZ(0)'
	}

	resize()
	update()

	$('#sellerSearch').on('input', function() {
		var mainval = $(this).val();

		if(mainval!=''){
			fetch('/processSeller', {
				method: 'POST',
				headers: {
					'Content-Type': 'application/json', // Set the Content-Type to JSON
				},
				body: JSON.stringify({ message: mainval }), // Convert the data to JSON format
			})
			.then(response => response.json())
			.then(data => {


				$('.messageRes').show();
				$('.statistics').hide();
				$('.productTable').show();

				if(data.response.statistics){
					$('.statistics').show();
					$('.statistics .total_questions').html(data.response.statistics.total_questions);
					$('.statistics .average_rating').html(data.response.statistics.average_rating);
					$('.statistics .average_price').html(data.response.statistics.average_price);
				}

				if(data.response.message){
					$('.messageRes').show();
					$('.messageResBody').html(data.response.message);
				}

				$("#productTableBody").empty();
				if (data.response.product_list.length > 0) {
					$('.productTable').show();
					data.response.product_list.forEach(function (product) {
						var row = "<tr>" +
							"<td>" + product["Product Title"] + "</td>" +
							"<td>" + product["Price"] + "</td>" +
							"<td>" + product["Brand"] + "</td>" +
							"<td>" + (product["Daraz Mall Status"] ? "Yes" : "No") + "</td>" +
							"<td>" + (product["Free Shipping Status"] ? "Yes" : "No") + "</td>" +
							"<td>" + product["No.of Questions"] + "</td>" +
							"<td>" + product["Rating"] + "</td>" +
							"<td>" + product["Seller Rating"] + "</td>" +
							"<td>" + product["Ship on Time Score"] + "</td>" +
							"<td class='text-end'>" +
							"<a href='" + product["URL Link"] + "' class='btn btn-sm btn-neutral'>View</a>" +
							"</td>" +
							"</tr>";

						
						$("#productTableBody").append(row);
					})
				}



				
			})
			.catch(error => console.error('Error:', error));
		}

	});
});
