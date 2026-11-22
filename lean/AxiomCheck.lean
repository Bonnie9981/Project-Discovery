import Discovery
import Lean

/-!
# Axiom check for every theorem under `Discovery`

Run in CI with `lake env lean AxiomCheck.lean`. Instead of a hand-written list,
this walks the compiled environment, so a newly added theorem cannot be skipped.

For each theorem it prints `AXIOMS <name>: [...]` and fails the build if any
axiom other than the three standard ones (`propext`, `Classical.choice`,
`Quot.sound`) is used — this includes `sorryAx`. CI then runs
`python -m discovery.lean_decls axioms.txt` to cross-check that every theorem
in the source files appears in this output.
-/

open Lean Elab Command

elab "#check_discovery_axioms" : command => do
  let env ← getEnv
  let allowed : List Name := [``propext, ``Classical.choice, ``Quot.sound]
  let mut names : Array Name := #[]
  for (name, ci) in env.constants.toList do
    if (`Discovery).isPrefixOf name && !name.isInternal then
      if let .thmInfo _ := ci then
        names := names.push name
  names := names.qsort Name.lt
  let mut bad : Array (Name × Name) := #[]
  for name in names do
    let axs ← collectAxioms name
    logInfo m!"AXIOMS {name}: {axs.toList}"
    for a in axs do
      unless allowed.contains a do
        bad := bad.push (name, a)
  logInfo m!"THEOREM_COUNT {names.size}"
  if names.isEmpty then
    throwError "no theorems found under Discovery"
  unless bad.isEmpty do
    throwError m!"non-standard axioms used: {bad.toList}"

#check_discovery_axioms
