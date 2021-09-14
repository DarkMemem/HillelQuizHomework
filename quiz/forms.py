from django.forms import BaseInlineFormSet, ModelForm, modelformset_factory
from django.core.exceptions import ValidationError
from django import forms
from .models import Choice, Question

from collections import Counter


class ChoiceInlineFormSet(BaseInlineFormSet):
    def clean(self):
        # lst = []
        # for form in self.forms:
        #     if form.cleaned_data['is_correct']:
        #         lst.append(1)
        #     else:
        #         lst.append(0)
        num_correct_answer = sum(1 for form in self.forms if form.cleaned_data['is_correct'])
        if num_correct_answer == 0:
            raise ValidationError("Нужно указать хотябы 1н правильный ответ")

        if num_correct_answer == len((self.forms)):
            raise ValidationError("Не могут все ответы быть правильными")


class QuestionInlineFormSet(BaseInlineFormSet):
    def clean(self):
        if not (self.instance.QUESTION_MIN_LIMIT <= len(self.forms) <= self.instance.QUESTION_MAX_LIMIT):
            raise ValidationError('Кол-во вопросов должно быть в диапазоне от {} до {}'.format(
                self.instance.QUESTION_MIN_LIMIT,
                self.instance.QUESTION_MAX_LIMIT
            ))

        lst = []
        for form in self.forms:
            lst.append(form.cleaned_data['order_num'])
        lst1 = Counter(lst)
        for item in lst1.values():
            if item > 1:
                raise ValidationError('Поле "Order num" долшжно быть уникальным!')
        if not 1 in lst:
            raise ValidationError('Поле "Order num" должно начинаться с единицы!')
        if len(lst) > 20:
            raise ValidationError('Количество вопросов не должно превышать 20ти!')
        lst2 = sorted(lst)
        if len(lst) != lst2[-1]:
            raise ValidationError('Шаг вопроса не должен превышать 1')


class ChoiceForm(ModelForm):
    is_selected = forms.BooleanField(required=False)

    class Meta:
        model = Choice
        fields = ['text']


ChoicesFormset = modelformset_factory(
    model=Choice,
    form=ChoiceForm,
    extra=0
)
