prompt = ""
prompt += """
            First, carefully analyze the image and extract the most critical features of the garment. Focus only on features that will help identify similar products in online searches. Think critically about each feature for 2 seconds before generating the output. Exclude any irrelevant details or features that cannot be reasonably inferred from the image.

            ### Step 1: Extract Key Features
            Please extract the following key features from the garment:
            1. **Category**: The general category of the garment (e.g., outerwear, dress, top, pants, etc.).
            2. **Gender**: Specify the intended gender for the garment (e.g., man, woman, unisex).
            3. **Garment Type**: The specific type of garment (e.g., bomber jacket, halter dress, t-shirt, hoodie).
            4. **Color**: Focus on the most dominant colors and describe them in detail. Use phrases like "solid navy blue", "black with white accents", or "light pink with floral print".
            5. **Pattern**: Include only if the garment has a prominent pattern (e.g., polka dots, stripes, floral). Skip if the garment is plain.
            6. **Additional Features**: Briefly mention one or two distinctive elements, such as "zippered front", "puff sleeves", "ruffled hem", or "side pockets". Focus on unique features that stand out visually.

            ### Step 2: Generate Description
            After identifying the key features, generate a concise and well-structured description of the garment. The description should prioritize **gender**, **color**, and **specific garment type**, as these are critical for finding the most relevant products online. Exclude any unnecessary or overly detailed features.

            ### Example Output:
            **Category**: Outerwear  
            **Gender**: Woman  
            **Garment Type**: Bomber Jacket  
            **Color**: Solid black with white accents  
            **Pattern**: None  
            **Additional Features**: Zippered front, ribbed cuffs  

            **Category**: Dress  
            **Gender**: Woman  
            **Garment Type**: Halter dress  
            **Color**: Dark navy blue with white polka dots  
            **Pattern**: Polka dots  
            **Additional Features**: Flared skirt, halter neckline  

            ### Guidelines:
            1. Focus only on features that matter for identifying similar garments online. Avoid including irrelevant details, like fabric texture or occasion, unless they are highly distinctive.
            2. Exclude references to people, backgrounds, or anything outside the garment itself.
            3. Ensure the description is concise and avoids excessive detail.

            The goal is to create a description optimized for Google search queries, helping users find similar garments quickly and accurately.
            """
