const form = document.querySelector('#form-signup');

async funtion signUser() {
	const form_data = new FormData(form);

	try {
		const response = await fetch('/auth/sign-up', {
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
