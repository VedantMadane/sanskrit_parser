from sanskrit_parser.generator.paninian_object import PaninianObject
from sanskrit_parser.generator.prakriya import Prakriya, PrakriyaVakya
from sanskrit_parser.generator.sutras_yaml import sutra_list
from indic_transliteration import sanscript

def run_test_case(input_padas, expected_output, tags=None):
    # Construct input objects
    inputs = []
    for i, p in enumerate(input_padas):
        obj = PaninianObject(p, encoding=sanscript.SLP1)
        # Apply manual tags if provided
        if tags and i < len(tags) and tags[i]:
            for t in tags[i]:
                obj.setTag(t)
        inputs.append(obj)

    # Add dummy object to allow processing of last element
    inputs.append(PaninianObject("", encoding=sanscript.SLP1))

    p = Prakriya(sutra_list, PrakriyaVakya(inputs))
    p.execute()
    output = p.output()
    # output is a list of lists of objects

    print(f"Input: {input_padas}, Tags: {tags}")
    # Convert output objects to strings (excluding dummy)
    output_strings = []
    for o_list in output:
        # Filter out empty dummy
        filtered = [o.canonical() for o in o_list if o.canonical() != ""]
        s = " ".join(filtered)
        output_strings.append(s)

    print(f"Output: {output_strings}")
    print(f"Expected: {expected_output}")

    matched = False
    for o in output_strings:
        if o.replace(" ", "") == expected_output.replace(" ", ""):
            matched = True
            break
    assert matched, f"Expected {expected_output}, got {output_strings}"

def test_1_1_14_nipata_ekajanag():
    # i + indra -> i indra (pragrhya)
    # Tag 'i' as nipata
    run_test_case(["i", "indra"], "i indra", tags=[["nipAta", "pada"], ["pada"]])

def test_1_1_14_negative():
    # aha (nipata, 2 vowels) + iti -> aheti (sandhi, NOT pragrhya)
    run_test_case(["aha", "iti"], "aheti", tags=[["nipAta", "pada"], ["pada"]])

def test_1_1_15_ot():
    # aho + iti -> aho iti (pragrhya)
    # Tag 'aho' as nipata
    run_test_case(["aho", "iti"], "aho iti", tags=[["nipAta", "pada"], ["pada"]])

def test_1_1_22_taraptamapau_gha():
    # kumAratara -> kumAratara (gha)
    tara = PaninianObject("tara", encoding=sanscript.SLP1)
    tara.setTag("tarap")

    p = Prakriya(sutra_list, PrakriyaVakya([tara, PaninianObject("", encoding=sanscript.SLP1)]))
    p.execute()
    # Check output for tag 'gha'
    out_obj = p.output()[0][0]
    assert out_obj.hasTag("gha"), f"Tags: {out_obj.tags}"

def test_1_1_26_ktaktavatu_nishtha():
    # gata -> gata (nishtha)
    kta = PaninianObject("ta", encoding=sanscript.SLP1)
    kta.setTag("kta")

    p = Prakriya(sutra_list, PrakriyaVakya([kta, PaninianObject("", encoding=sanscript.SLP1)]))
    p.execute()
    out_obj = p.output()[0][0]
    assert out_obj.hasTag("niSWA"), f"Tags: {out_obj.tags}"

def test_1_1_37_svaradi_nipata_avyaya():
    # svar -> avyaya
    svar = PaninianObject("svar", encoding=sanscript.SLP1)
    svar.setTag("svarAdi")

    p = Prakriya(sutra_list, PrakriyaVakya([svar, PaninianObject("", encoding=sanscript.SLP1)]))
    p.execute()
    out_obj = p.output()[0][0]
    assert out_obj.hasTag("avyaya"), f"Tags: {out_obj.tags}"

    # ca -> avyaya
    ca = PaninianObject("ca", encoding=sanscript.SLP1)
    ca.setTag("nipAta")
    p = Prakriya(sutra_list, PrakriyaVakya([ca, PaninianObject("", encoding=sanscript.SLP1)]))
    p.execute()
    out_obj = p.output()[0][0]
    assert out_obj.hasTag("avyaya"), f"Tags: {out_obj.tags}"

def test_1_1_41_avyayibhava_avyaya():
    # upakrSnam -> avyaya
    upa = PaninianObject("upakfznam", encoding=sanscript.SLP1)
    upa.setTag("avyayIbhAva")

    p = Prakriya(sutra_list, PrakriyaVakya([upa, PaninianObject("", encoding=sanscript.SLP1)]))
    p.execute()
    out_obj = p.output()[0][0]
    assert out_obj.hasTag("avyaya"), f"Tags: {out_obj.tags}"
