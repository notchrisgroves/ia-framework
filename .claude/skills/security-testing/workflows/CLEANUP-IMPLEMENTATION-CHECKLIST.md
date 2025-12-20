
## Phase 1: Core Scripts ✅ IN PROGRESS

### Documentation
- [x] Create comprehensive workflow documentation
  - File: `../workflows/cleanup-and-restoration.md`
  - Includes: Architecture, implementation specs, safety mechanisms
- [x] Update security testing workflow
  - File: `../SKILL.md`
  - Added: Phase 0 (state capture) and Phase 5 (cleanup)
- [x] Create quick reference card
  - File: `../CLEANUP-QUICKREF.md`
  - User-facing commands and troubleshooting

### State Capture Script
- [x] Create `../scripts/security/capture-engagement-state.py`
- [x] VPS state capture functionality
  - Disk usage across key directories
  - Bash history line count
  - Critical config file hashes (SHA256)
  - Docker container status
  - Open ports enumeration
  - Reaper database size
- [x] Local state capture functionality
  - Total disk usage and file count
  - Subdirectory breakdown
  - Temporary files identification
  - Credentials count
- [x] Backup creation for critical configs
- [x] Snapshot JSON generation and storage
- [x] UTF-8 encoding and Windows compatibility
- [ ] **TEST:** Run on airtable-bugbounty-2025-11
- [ ] **TEST:** Verify snapshots created correctly
- [ ] **TEST:** Check config backups on VPS

### Cleanup Plan Generator
- [x] Create `../scripts/security/generate-cleanup-plan.py`
- [x] VPS change analysis
  - Bash history growth detection
  - Modified config file detection (hash comparison)
  - Temporary file search (heuristic patterns)
  - Reaper database growth calculation
- [x] Local change analysis
  - Large directory identification
  - Compression potential calculation
  - Temporary file detection
- [x] Space savings estimation
- [x] Interactive plan display
- [x] Plan JSON output (`.cleanup-plan.json`)
- [ ] **TEST:** Generate plan for airtable-bugbounty-2025-11
- [ ] **TEST:** Verify space savings estimates
- [ ] **TEST:** Check file categorization accuracy

### VPS Cleanup Script
- [ ] Create `../scripts/security/cleanup-engagement-vps.sh`
- [ ] Delete temporary files
  - `/tmp/*scan*`, `/tmp/*temp*`
  - `/root/tools/*exploit*.py`
  - Pattern-based cleanup
- [ ] Secure delete credentials
  - Find all `.cookies/*`, `*cred*` files
  - Use `shred -vfz -n 3` (3-pass overwrite)
  - Log secure deletions
- [ ] Restore config files
  - Copy from `/root/.engagement-snapshots/[id]/`
  - Verify restoration with hash check
  - Log restored files
- [ ] Clean bash history
  - Keep lines up to snapshot count
  - Remove engagement-specific commands
  - Preserve history file integrity
- [ ] Clean Reaper database
  - Extract hostnames from engagement scope
  - `DELETE FROM requests WHERE hostname LIKE '%target%'`
  - `VACUUM` to reclaim space
  - Log deletion count
- [ ] Remove snapshot directory
  - Delete `/root/.engagement-snapshots/[id]/`
  - Confirm cleanup complete
- [ ] **TEST:** Dry-run on test engagement
- [ ] **TEST:** Verify restorations correct
- [ ] **TEST:** Check space reclaimed

### Local Cleanup Script
- [ ] Create `../scripts/security/cleanup-engagement-local.py`
- [ ] Archive large directories
  - Identify scan output directories
  - Create tar.gz archives
  - Verify archive integrity
  - Delete originals after verification
- [ ] Compress engagement directory
  - Create full `.tar.gz` of engagement
  - Calculate compression ratio
  - Verify archive extractable
- [ ] Delete temporary files
  - Remove from scratchpad
  - Pattern-based cleanup (`*.tmp`, `*-temp-*`)
  - Log deletions
- [ ] Preserve findings and reports
  - Never touch `05-findings/`
  - Never touch `06-reporting/`
  - Verify preservation after cleanup
- [ ] **TEST:** Run on test engagement
- [ ] **TEST:** Extract archive and verify
- [ ] **TEST:** Check findings preserved

### Main Orchestrator (DEFERRED)

**Status:** Manual cleanup workflow preferred over automated orchestrator.

**Current workflow:**
1. Run `generate-cleanup-plan.py` to create cleanup plan
2. Execute VPS cleanup commands from plan manually
3. Execute local cleanup commands from plan manually
4. Verify cleanup completed

**Future consideration:** If automated orchestrator needed, create `cleanup-engagement.py` with:
- [ ] Load cleanup plan from `.cleanup-plan.json`
- [ ] Interactive menu (5 options)
- [ ] Execute VPS cleanup (subprocess)
- [ ] Execute local cleanup (subprocess)
- [ ] Generate audit log (`.cleanup-log.json`)

---

## Phase 2: Change Tracking (OPTIONAL)

### Real-Time Monitoring Daemon
- [ ] Create `../scripts/security/track-engagement-changes.py`
- [ ] Filesystem monitoring (inotify on Linux)
- [ ] Change categorization
  - `temp_output` - scan results, temp files
  - `system_config` - modified configs
  - `engagement_tool` - custom scripts/exploits
  - `sensitive` - credentials, cookies, tokens
  - `installer` - tool installers
  - `logs` - bash history, application logs
- [ ] Change log generation (`.changes-log.json`)
- [ ] Daemon mode (background process)
- [ ] Graceful shutdown handling
- [ ] **TEST:** Monitor test session
- [ ] **TEST:** Verify categorization accuracy
- [ ] **TEST:** Check performance impact

---

## Phase 3: Integration Testing

### Test on Completed Engagement
- [ ] Choose test engagement: drumgrange-vdp-2025-11
- [ ] Create retroactive snapshot (manual documentation)
- [ ] Generate cleanup plan
- [ ] Review plan for accuracy
- [ ] Execute VPS cleanup (dry-run first)
- [ ] Execute local cleanup (dry-run first)
- [ ] Verify restoration successful
- [ ] Measure space savings
- [ ] Document lessons learned

### Test on New Engagement
- [ ] Start new small-scope engagement
- [ ] Capture state at beginning
- [ ] Run single testing session
- [ ] Generate cleanup plan
- [ ] Execute full cleanup
- [ ] Verify restoration
- [ ] Collect metrics (time, space, accuracy)

---

## Phase 4: Automation (FUTURE)

### Automatic Triggers
- [ ] Detect engagement completion (7 days no activity)
- [ ] Auto-generate cleanup plan
- [ ] Send notification (email or console)
- [ ] One-click cleanup from notification

### Integration Hooks
- [ ] Pre-engagement hook (auto-capture state)
- [ ] Post-engagement hook (auto-generate plan)
- [ ] Scheduled maintenance (monthly VPS cleanup)

---

## Metrics Collection

### Track These Metrics
- [ ] Time to complete cleanup (manual vs automatic)
- [ ] VPS space reclaimed per engagement
- [ ] Local space reclaimed per engagement
- [ ] Cleanup errors/mistakes count
- [ ] Credentials left on systems (target: 0)
- [ ] Configs not restored (target: 0)
- [ ] User satisfaction score

### Success Criteria
- [ ] Cleanup time: Manual (30-45 min) → Automatic (<5 min)
- [ ] Space savings: 3-6GB per engagement
- [ ] Error rate: <1% (99% accuracy)
- [ ] User satisfaction: 9/10 or higher

---

## Documentation Tasks

### User Documentation
- [x] Quick reference card
- [ ] Video tutorial (screen recording)
- [ ] FAQ document
- [ ] Troubleshooting guide

### Developer Documentation
- [ ] Code comments in all scripts
- [ ] Architecture diagram
- [ ] API documentation (function signatures)
- [ ] Contributing guide

---

## Testing Checklist

### Unit Tests
- [ ] State capture: VPS functionality
- [ ] State capture: Local functionality
- [ ] Cleanup plan: VPS analysis
- [ ] Cleanup plan: Local analysis
- [ ] VPS cleanup: File deletion
- [ ] VPS cleanup: Config restoration
- [ ] VPS cleanup: Bash history
- [ ] VPS cleanup: Reaper database
- [ ] Local cleanup: Archive creation
- [ ] Local cleanup: Compression
- [ ] Orchestrator: Menu system
- [ ] Orchestrator: Error handling

### Integration Tests
- [ ] Full workflow: Capture → Plan → Cleanup
- [ ] VPS-only cleanup
- [ ] Local-only cleanup
- [ ] Partial cleanup (user cancels mid-way)
- [ ] Rollback after failed cleanup
- [ ] Multiple engagements cleanup (batch)

### Edge Cases
- [ ] Engagement with no VPS usage (local only)
- [ ] Engagement with no local changes (VPS only)
- [ ] Snapshot missing (error handling)
- [ ] SSH connection fails (graceful degradation)
- [ ] Disk full during cleanup (error recovery)
- [ ] Corrupted snapshot file (validation)

---

## Rollback Testing

### VPS Rollback Scenarios
- [ ] Restore single config file
- [ ] Restore all configs from snapshot
- [ ] Rollback bash history cleanup
- [ ] Restore deleted files from backup
- [ ] Recovery from failed cleanup

### Local Rollback Scenarios
- [ ] Extract archive after compression
- [ ] Restore deleted temp files (from backup)
- [ ] Recover from corrupted archive
- [ ] Undo partial cleanup

---

## Production Readiness

### Before Going Live
- [ ] All Phase 1 scripts implemented
- [ ] All tests passing
- [ ] Documentation complete
- [ ] Tested on 3+ real engagements
- [ ] Zero unintended deletions
- [ ] User training completed
- [ ] Rollback procedures documented
- [ ] Emergency contact established

### Launch Checklist
- [ ] Announce to user (this is you!)
- [ ] Update CLAUDE.md with cleanup references
- [ ] Add to engagement README template
- [ ] Create slash command: `/cleanup`
- [ ] Schedule weekly cleanup review
- [ ] Set up metrics dashboard

---

## Known Issues & Limitations

### Current Limitations
- No real-time change tracking (Phase 1)
- Heuristic file detection (may miss some files)
- Manual approval required (not fully automatic)
- No multi-VPS support
- No cloud backup integration

### Future Enhancements
- ML-based file categorization
- Automatic hardening detection (config files)
- Cloud archive backup (S3/Azure)
- Multi-VPS coordinated cleanup
- Compliance reporting (SOC 2, ISO 27001)

---

## Progress Tracking

### Week 1 (2025-01-11 to 2025-01-17)
- [x] Documentation complete
- [x] State capture script implemented
- [x] Cleanup plan generator implemented
- [ ] VPS cleanup script in progress
- [ ] Local cleanup script in progress
- [ ] Testing on airtable engagement

### Week 2 (2025-01-18 to 2025-01-25)
- [ ] Orchestrator script implemented
- [ ] Full workflow tested
- [ ] Integration testing complete
- [ ] Production deployment
- [ ] Metrics collection started

---

## Notes

**2025-01-11:**
- Initial implementation started
- Documentation framework complete
- State capture and plan generator built
- Ready for testing phase

**Next Session:**
- Test state capture on airtable-bugbounty-2025-11
- Test cleanup plan generator
- Build VPS cleanup script if tests pass

---

**Status:** 40% Complete (Phase 1)
**Next Milestone:** VPS + Local cleanup scripts (Target: 2025-01-15)
**Final Milestone:** Production-ready system (Target: 2025-01-25)
