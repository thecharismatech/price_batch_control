Key Instructions for Writing Odoo 18:

1. Chatter Implementation:
   - Use simplified <chatter/> tag instead of oe_chatter div

2. View Definitions:
   - Use 'list' instead of 'tree' in view definitions
   - Update view_mode to use 'list' instead of 'tree'

3. Scheduled Actions:
   - Remove 'numbercall' field from ir.cron records

4. API Decorators:
   - Use new @api.readonly decorator for read-only operations

5. Search Functionality:
   - Implement _search_display_name instead of _name_search
   - Use advanced search capabilities across multiple fields

6. Access Control:
   - Use check_access() for combined rights/rules checking
   - Use has_access() for boolean access checks
   - Use _filtered_access() for filtering records with access

7. Translations:
   - Use env._() instead of _() for translations
   - Utilize LazyTranslate factory for efficient translations

8. SQL Operations:
   - Use standard SQL IN clause instead of inselect operator

9. Date Handling:
   - Use new granularities: month_number, quarter_number, week_number
   - Implement flexible date grouping across years

10. Field Properties:
    - Use aggregator instead of group_operator
    - Related fields with related_sudo=True can be grouped without storage

11. Database Operations:
    - Use execute_query() instead of _flush_search()

12. JavaScript RPC:
    - Use rpc instead of jsonrpc for network calls
    - Import from "@web/core/network/rpc"