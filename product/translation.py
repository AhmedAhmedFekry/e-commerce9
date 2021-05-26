from modeltranslation.translator import (
    translator,
    register,
    TranslationOptions,
)
from product.models import Product, Category


class ProductTranslationsOptions(TranslationOptions):
    fields = ("title", "description", "slug")
    required_languages = {
        "ar": ("title", "description"),
        "default": ("title", "description"),
    }
    # empty_values = {
    #     "title": "title",
    # }


class CategoryTranslationsOptions(TranslationOptions):
    fields = ("title", "slug")
    required_languages = {"ar": ("title",), "default": ("title",)}


translator.register(Product, ProductTranslationsOptions)
translator.register(Category, CategoryTranslationsOptions)