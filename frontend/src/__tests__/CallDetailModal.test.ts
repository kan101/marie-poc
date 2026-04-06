import { mount, flushPromises } from '@vue/test-utils'
import { describe, it, expect, vi, beforeEach } from 'vitest'
import CallDetailModal from '../components/CallDetailModal.vue'
import * as api from '../api'
import type { CallDetail } from '../api'

const mockCall: CallDetail = {
  id: 1,
  call_id: 'call_01',
  caller: {
    id: 1,
    first_name: 'Johanna',
    last_name: 'Schmidt',
    full_name: 'Johanna Schmidt',
    email: 'johanna.schmidt@gmail.com',
    phone_number: '+49 152 11223456',
  },
  duration_seconds: 125,
  duration_display: '2:05',
  caller_type: 'new_client',
  called_at: '2026-04-04T15:36:00Z',
  summary: 'Caller inquired about a family law matter.',
  audio_file: 'call_01.wav',
  urgent: false,
  urgent_reason: '',
  requires_appointment: true,
  follow_up_sent: true,
  transcript: 'Hello, I would like to speak to a lawyer about my case.',
  notes: '',
  created_at: '2026-04-04T15:36:00Z',
  updated_at: '2026-04-04T15:36:00Z',
  proposed_appointment: '2026-04-05T10:00:00Z',
}

describe('CallDetailModal', () => {
  beforeEach(() => {
    vi.spyOn(api, 'fetchCall').mockResolvedValue(mockCall)
    vi.spyOn(api, 'updateNotes').mockResolvedValue(mockCall)
  })

  it('shows loading spinner initially', () => {
    const wrapper = mount(CallDetailModal, {
      props: { callId: 1 },
      attachTo: document.body,
    })
    expect(wrapper.find('.animate-spin').exists()).toBe(true)
  })

  it('renders caller name after loading', async () => {
    const wrapper = mount(CallDetailModal, {
      props: { callId: 1 },
      attachTo: document.body,
    })
    await flushPromises()
    expect(wrapper.text()).toContain('Johanna Schmidt')
  })

  it('renders summary after loading', async () => {
    const wrapper = mount(CallDetailModal, {
      props: { callId: 1 },
      attachTo: document.body,
    })
    await flushPromises()
    expect(wrapper.text()).toContain('Caller inquired about a family law matter.')
  })

  it('renders transcript after loading', async () => {
    const wrapper = mount(CallDetailModal, {
      props: { callId: 1 },
      attachTo: document.body,
    })
    await flushPromises()
    expect(wrapper.text()).toContain('Hello, I would like to speak to a lawyer')
  })

  it('shows urgent banner for urgent calls', async () => {
    vi.spyOn(api, 'fetchCall').mockResolvedValue({
      ...mockCall,
      urgent: true,
      urgent_reason: 'Court deadline in 3 days.',
    })
    const wrapper = mount(CallDetailModal, {
      props: { callId: 1 },
      attachTo: document.body,
    })
    await flushPromises()
    expect(wrapper.text()).toContain('Urgent — callback required')
    expect(wrapper.text()).toContain('Court deadline in 3 days.')
  })

  it('emits close on overlay click', async () => {
    const wrapper = mount(CallDetailModal, {
      props: { callId: 1 },
      attachTo: document.body,
    })
    await flushPromises()
    await wrapper.find('.absolute.inset-0').trigger('click')
    expect(wrapper.emitted('close')).toBeTruthy()
  })

  it('emits close on escape key', async () => {
    const wrapper = mount(CallDetailModal, {
      props: { callId: 1 },
      attachTo: document.body,
    })
    await flushPromises()
    await wrapper.trigger('keydown', { key: 'Escape' })
    expect(wrapper.emitted('close')).toBeTruthy()
  })

  it('saves notes and shows saved confirmation', async () => {
    const wrapper = mount(CallDetailModal, {
      props: { callId: 1 },
      attachTo: document.body,
    })
    await flushPromises()
    await wrapper.find('textarea').setValue('Follow up on Monday')
    const buttons = wrapper.findAll('button')
    const saveButton = buttons.find(b => b.text().includes('Save notes'))
    await saveButton!.trigger('click')
    await flushPromises()
    expect(api.updateNotes).toHaveBeenCalledWith(1, 'Follow up on Monday')
  })
})