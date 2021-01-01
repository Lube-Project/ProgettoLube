import * as React from 'react';
export declare enum DropdownComponent {
    year = "year",
    month = "month",
    day = "day"
}
interface IProps {
    startDate?: string;
    endDate?: string;
    selectedDate?: string;
    order?: DropdownComponent[];
    onMonthChange?: Function;
    onDayChange?: Function;
    onYearChange?: Function;
    onDateChange?: Function;
    ids?: {
        year?: string;
        month?: string;
        day?: string;
    };
    names?: {
        year?: string;
        month?: string;
        day?: string;
    };
    classes?: {
        dateContainer?: string;
        yearContainer?: string;
        monthContainer?: string;
        dayContainer?: string;
        year?: string;
        month?: string;
        day?: string;
        yearOptions?: string;
        monthOptions?: string;
        dayOptions?: string;
    };
    defaultValues?: {
        year?: string;
        month?: string;
        day?: string;
    };
    options?: {
        yearReverse?: boolean;
        monthShort?: boolean;
        monthCaps?: boolean;
    };
}
interface IState {
    startYear: number;
    startMonth: number;
    startDay: number;
    endYear: number;
    endMonth: number;
    endDay: number;
    selectedYear: number;
    selectedMonth: number;
    selectedDay: number;
}
export declare class DropdownDate extends React.Component<IProps, IState> {
    renderParts: any;
    constructor(props: IProps);
    static getDerivedStateFromProps(nextProps: IProps, prevState: IState): {
        selectedYear: number;
        selectedMonth?: undefined;
        selectedDay?: undefined;
    } | {
        selectedMonth: number;
        selectedYear?: undefined;
        selectedDay?: undefined;
    } | {
        selectedDay: number;
        selectedYear?: undefined;
        selectedMonth?: undefined;
    } | null;
    generateYearOptions(): JSX.Element[];
    generateMonthOptions(): JSX.Element[];
    generateDayOptions(): JSX.Element[];
    handleDateChange: (type: DropdownComponent, value: number) => void;
    handleYearChange: (e: any) => void;
    handleMonthChange: (e: any) => void;
    handleDayChange: (e: any) => void;
    renderYear: () => JSX.Element;
    renderMonth: () => JSX.Element;
    renderDay: () => JSX.Element;
    render: () => JSX.Element;
}
export {};
