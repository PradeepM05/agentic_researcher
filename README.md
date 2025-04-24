DECLARE
    v_date DATE := TO_DATE('01-APR-2025', 'DD-MON-YYYY');
BEGIN
    WHILE v_date <= TO_DATE('20-APR-2025', 'DD-MON-YYYY') LOOP
        -- Skip weekends
        IF TO_CHAR(v_date, 'DY', 'NLS_DATE_LANGUAGE=ENGLISH') NOT IN ('SAT', 'SUN') THEN
            CDW_ACTIMIZE.SP_ADD_PARTITION('cdw_actimize', 'FI_PRICING_SCR_HIST', TO_CHAR(v_date, 'DD-Mon-YYYY'), 'Y', 'N', 'N');
        END IF;
        v_date := v_date + 1;
    END LOOP;
END;
/
