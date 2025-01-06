class CustomFormValidator: 
    def form_valid(self, form):
        prepcard = form.save(commit=False)
        formset = IngredientFormSet(self.request.POST)
        
        if formset.is_valid():
            ingredients = formset.save(commit=False)
                        
            for item in ingredients:
                item.card = prepcard
        else:
            formset.non_form_error().append("Ingredient Form is invalid")
            print("Error: Invalid Ingredient Form")
            return self.render_to_response(
                self.get_context_date(form=form, formset=formset)
            )
        
        prepcard.owner = self.request.user
        prepcard.save()
        
        for item in ingrediets:
            item.save()
        
        return super().form_valid(form)
    
    def form_invalid(self, form):
        formset = IngredientFormSet(self.request.POST)
        print("Error: Invalid Prepcard Form")
        return self.render_to_response(
            self.get_context_date(form=form, formset=formset)
        )