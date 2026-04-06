import { mount, flushPromises } from '@vue/test-utils'
import type { PaginatedResponse, CallSummary } from '../api'
import { describe, it, expect, vi, beforeEach } from 'vitest'
import CallList from '../components/CallList.vue'
import * as api from '../api'

const mockCalls: PaginatedResponse<CallSummary> = {
  count: 2,
  next: null,
  previous: null,
  results: [
    {
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
    },
    {
      id: 2,
      call_id: 'call_02',
      caller: {
        id: 2,
        first_name: 'Ahmed',
        last_name: 'Hassan',
        full_name: 'Ahmed Hassan',
        email: 'ahmed.hassan@gmail.com',
        phone_number: '+49 151 66123456',
      },
      duration_seconds: 29,
      duration_display: '0:29',
      caller_type: 'new_client',
      called_at: '2026-04-03T01:05:00Z',
      summary: 'Urgent matter regarding a court deadline.',
      audio_file: 'call_02.wav',
      urgent: true,
      urgent_reason: 'Caller mentioned a court hearing in 3 days.',
      requires_appointment: true,
      follow_up_sent: true,
      proposed_appointment: '2026-04-05T10:00:00Z',
    },
  ],
}

describe('CallList', () => {
    beforeEach(() => {
      vi.spyOn(api, 'fetchCalls').mockResolvedValue(mockCalls)
    })
  
    it('renders correct number of cards', async () => {
      const wrapper = mount(CallList, { props: { selectedId: null } })
      await flushPromises()
      const cards = wrapper.findAllComponents({ name: 'CallCard' })
      expect(cards).toHaveLength(2)
    })
  
    it('shows total call count', async () => {
      const wrapper = mount(CallList, { props: { selectedId: null } })
      await flushPromises()
      expect(wrapper.text()).toContain('2 calls total')
    })
  
    it('emits select event on card click', async () => {
      const wrapper = mount(CallList, { props: { selectedId: null } })
      await flushPromises()
      const cards = wrapper.findAllComponents({ name: 'CallCard' })
      await cards[0].trigger('click')
      expect(wrapper.emitted('select')).toBeTruthy()
      expect(wrapper.emitted('select')![0]).toEqual([1])
    })
  
    it('shows no calls message when empty', async () => {
      vi.spyOn(api, 'fetchCalls').mockResolvedValue({ count: 0, next: null, previous: null, results: [] })
      const wrapper = mount(CallList, { props: { selectedId: null } })
      await flushPromises()
      expect(wrapper.text()).toContain('No calls found')
    })
  
    it('passes search param to API', async () => {
      const wrapper = mount(CallList, { props: { selectedId: null } })
      await flushPromises()
      await wrapper.find('input').setValue('Johanna')
      await flushPromises()
      expect(api.fetchCalls).toHaveBeenCalledWith(expect.objectContaining({ search: 'Johanna' }))
    })
  })