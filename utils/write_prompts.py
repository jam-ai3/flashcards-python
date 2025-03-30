


WRITE_PROMPTS = {
    'IMPROVE_GRAMMER': lambda context, target_paragraph: (
        f"For the following context and target paragraph, improve the grammer of the target paragraph. "
        f"Context: {context} "
        f"Target Paragraph: {target_paragraph} "
        f"Respond in the following JSON format: [{{ 'improved': string }}]."
    )
}