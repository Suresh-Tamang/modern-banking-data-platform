{% macro generate_schema_name(custom_schema_name, node) -%}

    {%- set default_schema = target.schema -%}
    
    {# If a custom schema is provided in dbt_project.yml or a config block, use it exclusively #}
    {%- if custom_schema_name is not none -%}

        {{ custom_schema_name | trim }}

    {# If no custom schema is provided, fall back to the default (public) #}
    {%- else -%}

        {{ default_schema }}

    {%- endif -%}

{%- endmacro %}