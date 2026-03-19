import importlib.util
import pathlib
import sys
import unittest

SCRIPT = pathlib.Path('/Users/kjaylee/.openclaw/workspace/misskim-skills/skills/idea-factory-v2/scripts/idea_factory_v2.py')
spec = importlib.util.spec_from_file_location('idea_factory_v2', SCRIPT)
mod = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = mod
spec.loader.exec_module(mod)


class IdeaFactoryV2Tests(unittest.TestCase):
    def test_red_team_fields_exist_for_all_blueprints(self):
        for blueprint in mod.BLUEPRINTS:
            rt = mod.build_red_team(blueprint)
            self.assertIn('reject_risks', rt)
            self.assertIn('mitigations', rt)
            self.assertIn('verdict', rt)
            self.assertIn('penalty', rt)
            self.assertTrue(rt['mitigations'])
            self.assertIn(rt['verdict'], {'go', 'shrink', 'reject'})

    def test_overlap_rule_suppresses_shared_axes(self):
        base = mod.score_blueprint(mod.BLUEPRINTS[0], {k: 0 for k in mod.KEYWORD_TAGS})
        clone_bp = dict(mod.BLUEPRINTS[0])
        clone_bp['slug'] = 'listlens-clone'
        clone_bp['title'] = 'ListLens Clone'
        clone = mod.score_blueprint(clone_bp, {k: 0 for k in mod.KEYWORD_TAGS})
        overlap, meta = mod.ideas_overlap(base, clone)
        self.assertTrue(overlap)
        self.assertGreaterEqual(meta['shared_axes'], 2)

    def test_final_batch_non_overlap(self):
        scored = [mod.score_blueprint(bp, {k: 0 for k in mod.KEYWORD_TAGS}) for bp in mod.BLUEPRINTS]
        final_ideas, suppressed = mod.suppress_overlap(scored, desired_count=5)
        self.assertGreaterEqual(len(final_ideas), 5)
        for i, a in enumerate(final_ideas):
            for b in final_ideas[i+1:]:
                overlap, _ = mod.ideas_overlap(a, b)
                self.assertFalse(overlap)
        self.assertIsInstance(suppressed, list)


if __name__ == '__main__':
    unittest.main()
