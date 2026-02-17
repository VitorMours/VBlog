document.addEventListener('DOMContentLoaded', function () {
	const menuIcon = document.getElementById('menu-icon');
	const mobileMenu = document.getElementById('mobile-menu');
	const line1 = document.getElementById('line-1');
	const line2 = document.getElementById('line-2');
	const line3 = document.getElementById('line-3');

	function setClosed() {
		if (!mobileMenu) return;
		mobileMenu.style.maxHeight = '0';
		mobileMenu.style.opacity = '';
		mobileMenu.style.pointerEvents = 'none';
		if (menuIcon) menuIcon.setAttribute('aria-expanded', 'false');
		if (line1) { line1.style.transform = ''; }
		if (line2) { line2.style.opacity = ''; }
		if (line3) { line3.style.transform = ''; }
	}

	function setOpen() {
		if (!mobileMenu) return;
		mobileMenu.style.maxHeight = mobileMenu.scrollHeight + 'px';
		mobileMenu.style.opacity = '1';
		mobileMenu.style.pointerEvents = 'auto';
		if (menuIcon) menuIcon.setAttribute('aria-expanded', 'true');
		if (line1) { line1.style.transform = 'translateY(8px) rotate(45deg)'; }
		if (line2) { line2.style.opacity = '0'; }
		if (line3) { line3.style.transform = 'translateY(-8px) rotate(-45deg)'; }
	}

	if (menuIcon && mobileMenu) {
		// ensure aria attribute exists
		if (!menuIcon.hasAttribute('aria-expanded')) menuIcon.setAttribute('aria-expanded', 'false');
		menuIcon.addEventListener('click', function (e) {
			const expanded = menuIcon.getAttribute('aria-expanded') === 'true';
			if (expanded) setClosed(); else setOpen();
		});
		// keyboard toggling
		menuIcon.addEventListener('keydown', function (e) {
			if (e.key === 'Enter' || e.key === ' ' || e.key === 'Spacebar') {
				e.preventDefault();
				const expanded = menuIcon.getAttribute('aria-expanded') === 'true';
				if (expanded) setClosed(); else setOpen();
			}
		});

		// Close menu when resizing to large screens
		const mq = window.matchMedia('(min-width: 640px)');
		const mqHandler = (e) => { if (e.matches) setClosed(); };
		if (mq.addEventListener) mq.addEventListener('change', mqHandler);
		else if (mq.addListener) mq.addListener(mqHandler);
	}
});
