function my_scope() {
  const forms = document.querySelectorAll('.form-delete');

  for (const form of forms) {
    form.addEventListener('submit', (e) => {
      e.preventDefault();

      const confirmed = confirm('Are you sure?');
      if (confirmed) form.submit();

      return;
    });
  }
}

my_scope();
