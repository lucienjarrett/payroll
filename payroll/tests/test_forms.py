from .. import forms

class TestPostForm:
    def test_form(self):
        form = forms.PostForm(data={})
        assert form.is_valid() is False, "Should be invalid of no data given.."

        form = forms.PostForm(data={'Hello'})
        assert form.is_valid() is True, 'Should be valid if data is given'