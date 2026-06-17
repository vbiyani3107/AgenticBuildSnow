/**
 * Recreate or update: [SN-DO] Daily Top 10 Incidents List
 *
 * Run in: System Definition → Scripts - Background (Global scope)
 * Or via MCP: SN-Execute-Background-Script
 *
 * Optional: set UPDATE_SET_SYS_ID before running to capture in an Update Set.
 */
(function () {
    // --- Configuration (edit for target instance) ---
    var JOB_NAME = '[SN-DO] Daily Top 10 Incidents List';
    var RUN_TYPE = 'daily';
    var RUN_TIME = '1970-01-01 15:00:00'; // 3:00 PM — adjust if your instance TZ differs
    var TIME_ZONE = ''; // empty = instance default
    var ACTIVE = true;
    var UPDATE_SET_SYS_ID = ''; // e.g. 'ed8db115fb294790a5c9ff8165efdcbf' or leave blank

  var SCRIPT_BODY = [
        '// [SN-DO] Daily Top 10 Incidents List — read-only',
        "var LOG_PREFIX = '[SN-DO] Daily Top 10 Incidents List: ';",
        "var gr = new GlideRecord('incident');",
        "gr.orderByDesc('sys_created_on');",
        'gr.setLimit(10);',
        'gr.query();',
        'var count = 0;',
        'while (gr.next()) {',
        '    count++;',
        "    gs.info(LOG_PREFIX + count + ' | ' + gr.number + ' | ' + gr.getDisplayValue('state') + ' | ' + gr.short_description);",
        '}',
        "gs.info(LOG_PREFIX + 'Listed ' + count + ' incident(s).');"
    ].join('\n');

    // --- Set current Update Set (optional) ---
    if (UPDATE_SET_SYS_ID) {
        var us = new GlideUpdateSet();
        us.set(UPDATE_SET_SYS_ID);
        gs.info('Current Update Set: ' + us.get().name);
    }

    // --- Upsert scheduled job by name ---
    var gr = new GlideRecord('sysauto_script');
    gr.addQuery('name', JOB_NAME);
    gr.query();

    var isUpdate = gr.next();
    if (!isUpdate) {
        gr.initialize();
        gr.name = JOB_NAME;
    }

    gr.run_type = RUN_TYPE;
    gr.run_time = RUN_TIME;
    gr.time_zone = TIME_ZONE;
    gr.active = ACTIVE;
    gr.conditional = false;
    gr.condition = '';
    gr.script = SCRIPT_BODY;

    var id;
    if (isUpdate) {
        gr.setWorkflow(false);
        id = gr.update();
        gs.info('Updated sysauto_script: ' + JOB_NAME + ' sys_id=' + gr.getUniqueValue());
    } else {
        id = gr.insert();
        gs.info('Created sysauto_script: ' + JOB_NAME + ' sys_id=' + id);
    }

    // --- Verify ---
    var verify = new GlideRecord('sysauto_script');
    if (verify.get(isUpdate ? gr.getUniqueValue() : id)) {
        gs.info('Verify: active=' + verify.active + ' run_type=' + verify.run_type + ' run_time=' + verify.getValue('run_time'));
    }
})();
