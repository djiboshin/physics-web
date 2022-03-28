import { writable} from 'svelte/store';

export const seminars = writable({1: []});
export const currentWeekNum = writable(1);

