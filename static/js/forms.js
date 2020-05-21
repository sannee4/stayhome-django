window.onload = () => {
    const search = document.querySelector('.search__input');
    console.log(search);

    if (search) {
        search.addEventListener('keyup', e => {
            if (e.code === "Enter") {
                window.location.href = `?search_query=${document.querySelector('.search__input').value}`
            }
        });
    }

    const profileForm = document.querySelector('.profile-form__file-input_profile');
    if (profileForm) {
        profileForm.addEventListener('change', () => {
            document.querySelector('.profile-info__avatar-form').submit();
        });
    }
};