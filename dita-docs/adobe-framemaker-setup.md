# Adobe FrameMaker Setup Guide for DITA Content

## File Organization

Create the following folder structure:

```
stripe-api-testing/
├── stripe-api-testing.ditamap
├── concepts/
│   ├── testing-objectives.dita
│   └── test-coverage.dita
├── tasks/
│   ├── get-stripe-api-key.dita
│   ├── configure-postman.dita
│   └── create-test-cases.dita
├── reference/
│   ├── test-script-example.dita
│   └── test-results-summary.dita
└── troubleshooting/
    ├── authentication-fails.dita
    ├── payment-intent-fails.dita
    └── test-cards-dont-work.dita
```

## Opening in Adobe FrameMaker

### Method 1: Open the DITAMAP

1. Launch Adobe FrameMaker
2. Select **File > Open**
3. Navigate to your project folder
4. Select `stripe-api-testing.ditamap`
5. Click **Open**

The DITA Map Manager will open showing your complete content structure.

### Method 2: Open Individual Topics

1. Select **File > Open**
2. Navigate to any `.dita` file
3. Click **Open**
4. Edit the topic directly in FrameMaker's structured editor

## Publishing Your Content

### Generate PDF Output

1. In DITA Map Manager, right-click on `stripe-api-testing.ditamap`
2. Select **Generate Output > PDF**
3. Choose your transformation scenario:
   - **pdf** (basic PDF)
   - **pdf2** (advanced PDF with custom styling)
4. Configure output settings:
   - Output location
   - PDF filename
   - Template (if custom templates are available)
5. Click **Generate**

### Generate HTML5 Output

1. Right-click on the ditamap in DITA Map Manager
2. Select **Generate Output > HTML5**
3. Configure settings:
   - Output directory
   - Navigation style (top, side, etc.)
   - Search functionality
4. Click **Generate**

### Generate Responsive HTML5

1. Right-click on the ditamap
2. Select **Generate Output > Responsive HTML5**
3. This creates mobile-friendly documentation
4. Configure responsive breakpoints if needed
5. Click **Generate**

## Validating Your DITA Content

1. Open any DITA file in FrameMaker
2. Select **DITA > Validate**
3. Review any validation errors or warnings
4. Fix issues and re-validate

## Customizing the Output

### Using Templates

1. Select **File > New > Book from Template**
2. Choose a DITA template
3. Customize colors, fonts, and layouts
4. Save as a custom template
5. Reference your template when publishing

### Modifying the Ditamap

1. Open the ditamap in DITA Map Manager
2. Drag and drop to reorganize topics
3. Right-click to add new topicrefs
4. Add metadata for better SEO and discoverability

## Best Practices for Your Portfolio

1. **Show the DITAMAP structure** - This demonstrates your understanding of information architecture
2. **Include multiple topic types** - Concept, Task, Reference, and Troubleshooting show versatility
3. **Use proper DITA elements** - `<codeph>`, `<uicontrol>`, `<parmname>` show attention to semantic markup
4. **Generate multiple outputs** - PDF, HTML5, and Responsive HTML5 showcase your publishing skills
5. **Maintain consistent structure** - Well-organized folders and clear file naming

## Showcasing Your Skills

When presenting this work:

- **Explain your topic type choices**: Why you used troubleshooting vs. task topics
- **Demonstrate reuse**: Show how DITA enables content reuse across outputs
- **Discuss conditional publishing**: Explain how you could add profiling for different audiences
- **Show the relationship table**: If you create one, explain how it improves navigation
- **Present multiple outputs**: Show PDF and HTML side-by-side to demonstrate single-sourcing

## Additional FrameMaker Features to Explore

- **Conditional Text**: Create variants for different audiences
- **Variables**: Reuse product names and version numbers
- **Cross-references**: Link between topics dynamically
- **Key definitions**: Centralize terminology management
- **Relationship tables**: Create see-also links automatically
