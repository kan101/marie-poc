import { mount } from '@vue/test-utils'
import { describe, it, expect } from 'vitest'
import CallCard from '../components/CallCard.vue'
import type { CallSummary } from '../api'

const baseCall: CallSummary = {
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
  proposed_appointment: '2026-04-05T10:00:00Z',
}

describe('CallCard', () => {
  it('renders caller name', () => {
    const wrapper = mount(CallCard, {
      props: { call: baseCall, selected: false },
    })
    expect(wrapper.text()).toContain('Johanna Schmidt')
  })

  it('renders caller email', () => {
    const wrapper = mount(CallCard, {
      props: { call: baseCall, selected: false },
    })
    expect(wrapper.text()).toContain('johanna.schmidt@gmail.com')
  })

  it('renders phone number', () => {
    const wrapper = mount(CallCard, {
      props: { call: baseCall, selected: false },
    })
    expect(wrapper.text()).toContain('+49 152 11223456')
  })

  it('renders summary', () => {
    const wrapper = mount(CallCard, {
      props: { call: baseCall, selected: false },
    })
    expect(wrapper.text()).toContain('Caller inquired about a family law matter.')
  })

  it('shows email sent badge', () => {
    const wrapper = mount(CallCard, {
      props: { call: baseCall, selected: false },
    })
    expect(wrapper.text()).toContain('Email sent')
  })

  it('shows urgent badge when urgent', () => {
    const wrapper = mount(CallCard, {
      props: {
        call: { ...baseCall, urgent: true, urgent_reason: 'Court deadline in 3 days.' },
        selected: false,
      },
    })
    expect(wrapper.text()).toContain('Urgent')
  })

  it('does not show urgent badge when not urgent', () => {
    const wrapper = mount(CallCard, {
      props: { call: baseCall, selected: false },
    })
    expect(wrapper.text()).not.toContain('Urgent')
  })

  it('shows new client badge', () => {
    const wrapper = mount(CallCard, {
      props: { call: baseCall, selected: false },
    })
    expect(wrapper.text()).toContain('New client')
  })

  it('shows existing client badge', () => {
    const wrapper = mount(CallCard, {
      props: {
        call: { ...baseCall, caller_type: 'existing_client' },
        selected: false,
      },
    })
    expect(wrapper.text()).toContain('Existing client')
  })

  it('emits select event with call id on click', async () => {
    const wrapper = mount(CallCard, {
      props: { call: baseCall, selected: false },
    })
    await wrapper.find('div').trigger('click')
    expect(wrapper.emitted('select')).toBeTruthy()
    expect(wrapper.emitted('select')![0]).toEqual([1])
  })

  it('shows initials in avatar', () => {
    const wrapper = mount(CallCard, {
      props: { call: baseCall, selected: false },
    })
    expect(wrapper.text()).toContain('JS')
  })
})