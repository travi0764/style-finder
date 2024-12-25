prompt = ""
prompt += """
            First, carefully analyze the image and extract all the following features. Think critically about each feature for 2 seconds before generating the output. Only include features that are actually present in the garment or can be reasonably inferred from the image. If a feature is absent or irrelevant, exclude it from the final description.

            ### Step 1: Extract Features
            Please extract the following features from the garment:
            1. **Category**: The general category of the garment (e.g., outerwear, jacket, coat, blazer, cardigan, etc.).
            2. **Gender**: Specify the gender for which the garment is intended (e.g., man, woman, unisex).
            3. **Garment Type**: The specific garment type (e.g., bomber jacket, trench coat, blazer, puffer, hoodie, jumpsuit, etc.).
            4. **Color**: Describe the color(s) in as much detail as possible. For example, instead of just saying "brown", say "dark chocolate brown with a matte finish" or "light beige with a soft peach undertone".
            5. **Pattern**: Mention the pattern or print on the garment (e.g., plain, striped, checkered, floral, plaid, houndstooth, etc.).
            6. **Style**: The style of the garment, including any specific cut or silhouette details (e.g., "slim fit", "oversized", "tailored", "cropped").
            7. **Fit**: The fit of the garment (e.g., "relaxed fit", "regular fit", "loose fit").
            8. **Fabric/Material**: Describe the fabric in great detail (e.g., "100% wool", "soft cotton blend", "denim", "faux leather").
            9. **Texture**: Include the texture of the fabric (e.g., "smooth", "rough", "soft").
            10. **Closure Type**: Describe the closure mechanism (e.g., "button-down", "zippered", "snap-button").
            11. **Neckline/Collar**: Provide details of the neckline or collar type (e.g., "notched collar", "high-neck", "V-neck").
            12. **Sleeve Type**: Describe the sleeves (e.g., "long sleeves", "short sleeves").
            13. **Pockets**: Detail the number, type, and placement of pockets (e.g., "two front patch pockets", "side zippered pockets").
            14. **Additional Design Features**: Include any distinctive features, like logos, patches, embroidery.
            15. **Length**: Describe the length of the garment (e.g., "waist-length", "knee-length").
            16. **Lining**: If applicable, describe the lining material (e.g., "fully lined with satin").
            17. **Branding or Logos**: Note any visible logos or branding details (e.g., "small 'Adidas' logo").
            18. **Gender-Specific Details**: If the garment is designed for a specific gender, include how it is tailored for that gender.
            19. **Occasion/Use**: Describe if the garment is designed for a specific occasion or activity (e.g., "casual wear", "business attire").

            ### Step 2: Generate Description
            After identifying the features that are present, generate a final description by including only the relevant features. Exclude any features that are missing, irrelevant, or cannot be inferred from the image.

            ### Example Output:
            **Category**: Outerwear  
            **Garment Type**: Bomber Jacket  
            **Color**: Deep forest green with a matte finish  
            **Pattern**: Solid, no pattern  
            **Style**: Oversized, cropped length  
            **Fit**: Relaxed fit  
            **Fabric/Material**: 100% Nylon  
            **Texture**: Smooth  
            **Closure Type**: Zippered  
            **Additional Design Features**: Ribbed cuffs with contrasting colors  

            Note: Avoid including any references to the background or people in the image. The output should focus solely on the garment to assist in online search or cataloging purposes.
        """
