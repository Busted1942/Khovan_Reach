import os


def test_dillon_opening_briefing_is_scheduled():
    root = os.path.dirname(os.path.dirname(__file__))
    main_path = os.path.join(root, 'scripts', 'main.mast')
    qualification_path = os.path.join(root, 'scripts', 'act_1_qualification.mast')

    with open(main_path, 'r', encoding='utf-8') as f:
        main_text = f.read()
    with open(qualification_path, 'r', encoding='utf-8') as f:
        qual_text = f.read()

    assert 'await task_schedule(scene_01_departure_and_briefing)' in main_text, (
        'Mission start does not schedule the departure-and-briefing scene in scripts/main.mast'
    )
    assert 'task_schedule(khovan_reach_play_dillon_opening_text' in qual_text, (
        'The opening briefing task is not scheduled in scripts/act_1_qualification.mast'
    )
    assert 'Opening Briefing' in qual_text, (
        'The opening briefing message text is not present in scripts/act_1_qualification.mast'
    )
