const form = document.querySelector('#form-login');

async funtion loginUser() {
	const form_data = new FormData(form);

	try {
		const response = await fetch('/auth/login', {
			method: 'POST',
			body: form_data,
		});
		console.log(await response);
	} catch(e) {
		console.error(e);
	}

	window.location.replace('/');
}

form.addEventListener('submit', (event) => {
	event.preventDefault();
	signUser();
});
